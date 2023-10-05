from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

from time import sleep
import subprocess
from devgoldyutils import Colours

from .player import Player, PlayerNotFound, PlayerNotSupported

__all__ = ("VLC",)


class VLC(Player):
    def __init__(self, config: Config) -> None:
        super().__init__(Colours.ORANGE.apply("VLC"), config)

    def play(self, media: Media) -> subprocess.Popen:
        """Plays this media in the VLC media player."""

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

    
        elif self.platform == "iOS":
            self.logger.info("Detected your using iOS. \r\n")

            print(
                f"\033]vlc-x-callback://x-callback-url/stream?url={media.url}\033\\-------------------------\n- Tap to open VLC -\n-------------------------\033]8;;\033\\\n"
            )

            self.logger.info("Sleeping for 10 Seconds.")

            sleep(10)

        raise PlayerNotSupported(self, self.platform)