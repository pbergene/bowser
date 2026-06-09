# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Bowser is a URL-dispatching browser router for Linux. It registers itself as the system default browser (via `xdg-mime`) and routes each incoming URL to the right browser based on glob-matched hostname rules in a TOML config file.

## Running and testing

There is no test suite or linter config. Test manually:

```bash
# Run directly from the repo (without installing)
python3 bowser.py https://example.com
python3 bowser.py https://internal.work.com/dashboard

# After installation, use the wrapper
bowser https://example.com
```

Install to `~/.local/`:
```bash
bash install.sh
```

Verify registration:
```bash
xdg-settings get default-web-browser   # should print: bowser.desktop
```

## Architecture

```
bowser.py               Entry point — loads config, parses URL hostname, dispatches
browsers/__init__.py    REGISTRY dict + get_browser() factory
browsers/base.py        BrowserBase ABC — __init__ reads command/flags from config, open() calls subprocess.Popen
browsers/chrome.py      ChromeBrowser(BrowserBase)
browsers/edge.py        EdgeBrowser(BrowserBase)
config/config.toml      Bundled default config — copied to ~/.config/bowser/config.toml on first run
install.sh              Copies files to ~/.local/lib/bowser/, creates ~/.local/bin/bowser wrapper, registers desktop entry
bowser.desktop          XDG desktop entry (Exec path rewritten by install.sh)
```

**Dispatch flow:** `URL → urlparse → hostname → fnmatch rules (top-to-bottom, first match wins) → browser name → get_browser() → subprocess.Popen`

**Config location at runtime:** `~/.config/bowser/config.toml` (the repo's `config/config.toml` is the install-time source only).

**No external dependencies** — stdlib only (`tomllib`, `urllib`, `fnmatch`, `subprocess`). Requires Python 3.11+ for `tomllib`.

## Adding a browser

1. Create `browsers/<name>.py` subclassing `BrowserBase` — set `DEFAULT_COMMAND` and implement the `name` property.
2. Import the class and add it to `REGISTRY` in `browsers/__init__.py`.
3. Add a `[browsers.<name>]` section to `config/config.toml` (and to the user's `~/.config/bowser/config.toml`).
4. Re-run `install.sh` to push updated files to `~/.local/lib/bowser/`.
