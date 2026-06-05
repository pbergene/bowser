"""Microsoft Edge browser module."""

from __future__ import annotations

from typing import Any

from .base import BrowserBase


class EdgeBrowser(BrowserBase):
    DEFAULT_COMMAND = "microsoft-edge"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    @property
    def name(self) -> str:
        return "edge"
