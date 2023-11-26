from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging

from devgoldyutils import Colours

from .logger import mov_cli_logger

__all__ = ("MovCliException",)

class MovCliException(Exception):
    """Raises whenever there's a known error in mov-cli."""
    def __init__(self, message: str, logger: logging.Logger = None):
        message = Colours.RED.apply_to_string(message)

        if logger is None:
            logger = mov_cli_logger

        logger.critical(message)
        super().__init__(message)