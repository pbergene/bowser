"""Google Chrome browser module."""

from __future__ import annotations

from typing import Any

from .base import BrowserBase


class ChromeBrowser(BrowserBase):
    DEFAULT_COMMAND = "google-chrome"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    @property
    def name(self) -> str:
        return "chrome"
