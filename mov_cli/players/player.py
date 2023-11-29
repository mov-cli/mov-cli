from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config
    from ..utils.platform import SUPPORTED_PLATFORMS

import subprocess
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter

from .. import utils
from ..logger import mov_cli_logger

__all__ = ("Player",)

class Player(ABC):
    """A base class for all players in mov-cli."""
    def __init__(self, display_name: str, config: Config) -> None:
        self.display_name = display_name
        """Display name of player."""
        self.config = config
        """Mov-cli configuration."""
        self.platform: SUPPORTED_PLATFORMS = (
            utils.what_platform()
        ) # TODO: I might move this somewhere more centralized in the future. I'm not sure at the moment.
        """Operating system this device is running."""

        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.display_name)

        super().__init__()

    @abstractmethod
    def play(self, media: Media) -> subprocess.Popen:
        """Method to be overridden with code to play media in that specific player."""
        ...