from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from .players import Player
    from .utils.platform import SUPPORTED_PLATFORMS

from devgoldyutils import Colours
from .logger import mov_cli_logger

class MovCliException(Exception):
    """Raises whenever there's a known error in mov-cli."""
    def __init__(self, message: str, logger: logging.Logger = None):
        message = Colours.RED.apply_to_string(message)

        if logger is None:
            logger = mov_cli_logger

        logger.critical(message)
        super().__init__(message)


class PlayerNotFound(MovCliException):
    """Raised when player is not found."""
    def __init__(self, player: Player) -> None:
        super().__init__(
            f"The '{player.display_name}' player was not found. Are you sure you have it installed? " \
            "Are you sure the environment variable is set correctly?"
        )

class PlayerNotSupported(MovCliException):
    """Raised when player is not supported on that specific platform."""
    def __init__(self, player: Player, platform: SUPPORTED_PLATFORMS) -> None:
        super().__init__(
            f"The '{player.display_name}' player is not supported on '{platform}'. " \
            "We recommend VLC for iOS and MPV for every other platform."
        )