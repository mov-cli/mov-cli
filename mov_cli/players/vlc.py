from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

import subprocess
from devgoldyutils import Colours

from .player import Player, PlayerNotFound, PlayerNotSupported

__all__ = ("VLC",)

class VLC(Player):
    def __init__(self, config: Config) -> None:
        super().__init__(Colours.ORANGE.apply("VLC"), config)

    def play(self, media: Media) -> subprocess.Popen:
        """Plays this media in the VLC media player."""

        self.logger.info("Launching VLC Media Player...")

        if self.platform == "Linux" or self.platform == "Windows":
            try:
                return subprocess.Popen(
                    [
                        "vlc",
                        f'--http-referrer="{media.referrer}"',
                        f'"{media.url}"',
                        f'--meta-title="mov-cli:{media.title}"',
                        "--no-terminal",
                    ]
                )

            except ModuleNotFoundError:
                raise PlayerNotFound(self)

        raise PlayerNotSupported(self, self.platform)