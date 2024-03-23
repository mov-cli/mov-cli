from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media

import subprocess
from devgoldyutils import Colours, LoggerAdapter

from .. import errors
from ..logger import mov_cli_logger
from .player import Player

__all__ = ("CustomPlayer",)

logger = LoggerAdapter(mov_cli_logger, prefix = Colours.GREY.apply("CustomPlayer"))

class CustomPlayer(Player):
    """
    This player is invoked if you set a player that is not supported by mov-cli in the config, allowing users to invoke their own players.
    """
    def __init__(self, player_command: str, **kwargs) -> None:
        self.player_command = player_command

        super().__init__(**kwargs)

    def play(self, media: Media) -> subprocess.Popen:
        """Plays this media in a custom player."""
        logger.info(f"Launching your custom media player '{self.player_command}'...")

        try:
            return subprocess.Popen(
                [self.player_command, media.url]
            )
        except ModuleNotFoundError:
            raise errors.PlayerNotFound(self)