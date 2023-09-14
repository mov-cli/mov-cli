from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config
    from ..utils.platform import SUPPORTED_PLATFORMS

import subprocess
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter

from .. import utils, errors
from ..logger import mov_cli_logger

__all__ = ("Player", "PlayerNotFound", "PlayerNotSupported")


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


class PlayerNotFound(errors.MovCliException):
    """Raised when player is not found."""
    def __init__(self, player: Player) -> None:
        super().__init__(
            f"The '{player.display_name}' player was not found. Are you sure you have it installed? " \
            "Are you sure the environment variable is set correctly?"
        )

class PlayerNotSupported(errors.MovCliException):
    """Raised when player is not supported on that specific platform."""
    def __init__(self, player: Player, platform: SUPPORTED_PLATFORMS) -> None:
        super().__init__(
            f"The '{player.display_name}' player is not supported on '{platform}'. " \
            "We recommend VLC for iOS and MPV for every other platform."
        )