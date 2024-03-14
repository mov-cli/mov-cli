from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

import time
import subprocess
from devgoldyutils import Colours

from .. import errors
from .player import Player

__all__ = ("MPV",)

class MPV(Player):
    def __init__(self, config: Config) -> None:
        self.config = config
        super().__init__(Colours.PURPLE.apply("MPV"), config)

    def play(self, media: Media) -> subprocess.Popen:
        """Plays this media in the MPV media player."""

        self.logger.info("Launching MPV Media Player...")

        if self.platform == "Android":
            self.logger.info("Detected you're using Android.")

            return subprocess.Popen(
                [
                    "am",
                    "start",
                    "-n",
                    "is.xyz.mpv/is.xyz.mpv.MPVActivity",
                    "-e",
                    "filepath",
                    media.url,
                ]
            )

        elif self.platform == "iOS":
            # TODO: This should be moved to the VLC player class as it's invoking vlc not mpv.
            self.logger.info("Detected your using iOS. \r\n")

            print(
                f"\e]8;;vlc-x-callback://x-callback-url/stream?url={media.url}\e\\-------------------------\n- Tap to open VLC -\n-------------------------\e]8;;\e\\\n"
            )

            self.logger.info("Sleeping for 10 Seconds.")

            time.sleep(10)

        else:  # Windows, Linux and Other

            try:
                if self.platform == "Linux" or self.platform == "Windows":
                    mpv_args = [
                        f"--referrer={media.referrer}",
                        media.url,
                        f"--force-media-title={media.display_name}",
                        "--no-terminal",
                    ]

                    return subprocess.Popen(["mpv"] + mpv_args)

                elif self.platform == "Darwin":
                    return subprocess.Popen(
                        [
                            "iina",
                            "--no-stdin",
                            "--keep-running",
                            f"--mpv-referrer={media.referrer}",
                            media.url,
                            f"--mpv-force-media-title={media.display_name}",
                        ]
                    )

                raise errors.PlayerNotSupported(self, self.platform)

            except ModuleNotFoundError:
                raise errors.PlayerNotFound(self)
