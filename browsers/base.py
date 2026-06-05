"""Abstract base class for browser implementations."""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from typing import Any


class BrowserBase(ABC):
    """Base class every browser module must subclass."""

    #: Override in subclasses with the default system command.
    DEFAULT_COMMAND: str

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Args:
            config: The ``[browsers.<name>]`` section from config.toml,
                    e.g. ``{"command": "google-chrome", "flags": ["--incognito"]}``.
        """
        self.command: str = config.get("command", self.DEFAULT_COMMAND)
        self.flags: list[str] = config.get("flags", [])

    def open(self, url: str) -> None:
        """Launch the browser with *url*."""
        subprocess.Popen([self.command, *self.flags, url])

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier used in config and log messages."""
