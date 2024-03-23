from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from ..media import Media
    from ..utils.platform import SUPPORTED_PLATFORMS

import subprocess
from devgoldyutils import Colours, LoggerAdapter

from .. import errors
from ..logger import mov_cli_logger
from .player import Player

__all__ = ("VLC",)

logger = LoggerAdapter(mov_cli_logger, prefix = Colours.ORANGE.apply("VLC"))

class VLC(Player):
    def __init__(self, platform: SUPPORTED_PLATFORMS, **kwargs) -> None:
        self.platform = platform

        super().__init__(**kwargs)

    def play(self, media: Media) -> Optional[subprocess.Popen]:
        """Plays this media in the VLC media player."""

        logger.info("Launching VLC Media Player...")

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

        elif self.platform == "iOS":
            logger.debug("Detected your using iOS. \r\n")

            with open('/dev/clipboard', 'w') as f:
                f.write(f"vlc://{media.url}")

            logger.info("The URL was copied into your clipboard. To play it, open a browser and paste the URL.")

            return None # TODO: Idk what we can do here as for ios we don't return a subprocess.Popen. 
                        # Leaving it like so will print an error from the cli stating the player is not supported.
                        # I'll leave it to you Ananas. At least it doesn't raise an exception now. ~ Goldy

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

        return None