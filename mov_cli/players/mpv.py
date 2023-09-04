from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

import sys
import subprocess
from devgoldyutils import Colours

from .. import Config
from .player import Player, PlayerNotFound, PlayerNotSupported

__all__ = ("MPV",)

# NOTE: Incomplete code.

class MPV(Player):
    def __init__(self, config: Config) -> None:
        super().__init__(Colours.PURPLE.apply("MPV"), config)

    def play(self, media: Media) -> subprocess.Popen:
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
                    f"{media.url}",
                ]
            )

        elif self.platform == "iOS":
            self.logger.info("Detected your using iOS. \r\n")

            print(
                f"\033]8;;outplayer://{media.url}\033\\-------------------------\n- Tap to open Outplayer -\n-------------------------\033]8;;\033\\\n"
            )

            sys.exit(1) # NOTE: Is this needed? ~ Goldy

        else: # Windows, Linux and Other

            try:
                if self.platform == "Linux" or self.platform == "Windows":
                    mpv_args = [
                        f"--referrer={media.referrer}",
                        f"{media.url}",
                        f"--force-media-title=mov-cli:{media.title}",
                        "--no-terminal",
                    ]

                    if self.config.flatpak_mpv and self.platform == "Linux":  # Support for MPV on Flatpak.
                        self.logger.info("Using flatpak installation of MPV.")
                        return subprocess.Popen(
                            ["flatpak", "run", "io.mpv.Mpv"] + mpv_args
                        )

                    return subprocess.Popen(["mpv"] + mpv_args)

                elif self.platform == "Darwin":
                    return subprocess.Popen(
                        [
                            "iina",
                            "--no-stdin",
                            "--keep-running",
                            f"--mpv-referrer={media.referrer}",
                            media.url,
                            f"--mpv-force-media-title=mov-cli:{media.title}",
                        ]
                    )

                raise PlayerNotSupported(self, self.platform)

            except ModuleNotFoundError:
                raise PlayerNotFound(self)