"""Browser registry and factory.

To add a new browser:
1. Create ``browsers/<name>.py`` subclassing ``BrowserBase``.
2. Import it here and add it to ``REGISTRY``.
3. Add a ``[browsers.<name>]`` section in your config.toml.
"""

from __future__ import annotations

from typing import Any

from .base import BrowserBase
from .chrome import ChromeBrowser
from .edge import EdgeBrowser

# Map config name → browser class.  Add new browsers here.
REGISTRY: dict[str, type[BrowserBase]] = {
    "chrome": ChromeBrowser,
    "edge": EdgeBrowser,
}


def get_browser(name: str, browser_configs: dict[str, Any]) -> BrowserBase:
    """Return an instantiated browser for *name* using its config section.

    Args:
        name: Key from ``REGISTRY`` (e.g. ``"chrome"``).
        browser_configs: The full ``[browsers]`` table from config.toml.

    Raises:
        KeyError: If *name* is not in the registry.
    """
    if name not in REGISTRY:
        known = ", ".join(sorted(REGISTRY))
        raise KeyError(f"Unknown browser {name!r}. Known browsers: {known}")
    cls = REGISTRY[name]
    section = browser_configs.get(name, {})
    return cls(section)
