from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

import subprocess
from devgoldyutils import Colours

from .. import errors
from .player import Player

__all__ = ("VLC",)

class VLC(Player):
    def __init__(self, config: Config) -> None:
        super().__init__(Colours.ORANGE.apply("VLC"), config)

    def play(self, media: Media) -> subprocess.Popen:
        """Plays this media in the VLC media player."""

        self.logger.info("Launching VLC Media Player...")

        if self.platform == "Android":
            return subprocess.Popen(
                [
                    "am",
                    "start",
                    "-n",
                    "org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity",
                    "-e",
                    "title",
                    media.display_name,
                    media.url,
                ]
            )

        elif self.platform == "Linux" or self.platform == "Windows":
            try:
                args = [
                    "vlc", 
                    f'--meta-title="{media.display_name}"', 
                    media.url
                ]

                if media.referrer is not None:
                    args.append(f'--http-referrer="{media.referrer}"')

                return subprocess.Popen(args)

            except ModuleNotFoundError:
                raise errors.PlayerNotFound(self)

        raise errors.PlayerNotSupported(self, self.platform)