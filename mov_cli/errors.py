from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from .players import Player

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

# NOTE: I might remove this. ~ Goldy
class PlayerNotFound(MovCliException):
    """Raised when player is not found."""
    def __init__(self, player: Player) -> None:
        super().__init__(
            f"The player '{player.__class__.__name__}' was not found. Are you sure you have it installed? " \
            "Are you sure the environment variable is set correctly?"
        )