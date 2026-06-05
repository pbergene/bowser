#!/usr/bin/env python3
"""Bowser — URL-dispatching browser router.

Usage:
    bowser <url>

Bowser reads ~/.config/bowser/config.toml, matches the URL hostname against
the configured rules (first match wins), and launches the appropriate browser.
Falls back to ``default_browser`` when no rule matches.
"""

from __future__ import annotations

import fnmatch
import shutil
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlparse

# Paths
CONFIG_DIR = Path.home() / ".config" / "bowser"
CONFIG_FILE = CONFIG_DIR / "config.toml"
BUNDLED_CONFIG = Path(__file__).parent / "config" / "config.toml"


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy(BUNDLED_CONFIG, CONFIG_FILE)
        print(f"bowser: created default config at {CONFIG_FILE}", file=sys.stderr)
    with CONFIG_FILE.open("rb") as fh:
        return tomllib.load(fh)


def match_browser(hostname: str, rules: list[dict]) -> str | None:
    """Return the browser name for the first rule whose pattern matches *hostname*."""
    for rule in rules:
        pattern = rule.get("pattern", "")
        if fnmatch.fnmatch(hostname, pattern):
            return rule["browser"]
    return None


def dispatch(url: str) -> None:
    # Import here so browsers/ is resolved relative to this script's location.
    sys.path.insert(0, str(Path(__file__).parent))
    from browsers import get_browser  # noqa: PLC0415

    config = load_config()
    default = config.get("default_browser", "chrome")
    rules: list[dict] = config.get("rules", [])
    browser_configs: dict = config.get("browsers", {})

    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    browser_name = match_browser(hostname, rules) or default
    browser = get_browser(browser_name, browser_configs)
    browser.open(url)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: bowser <url>", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    try:
        dispatch(url)
    except KeyError as exc:
        print(f"bowser: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"bowser: unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
