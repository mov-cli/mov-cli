from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from ..config import Config

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
            self.logger.debug("Detected your using iOS. \r\n")

            with open('/dev/clipboard', 'w') as f:
                f.write(f"vlc://{media.url}")

            self.logger.info("The URL was copied into your clipboard. To play it, open a browser and paste the URL.")

        else:  # Windows, Linux and Other

            try:
                if self.platform == "Linux" or self.platform == "Windows":
                    args = [
                        "mpv",
                        media.url,
                        f"--force-media-title={media.display_name}",
                        "--no-terminal",
                    ]

                    if media.referrer is not None:
                        args.append(f"--referrer={media.referrer}")

                    return subprocess.Popen(args)

                elif self.platform == "Darwin":
                    args = [
                        "iina",
                        "--no-stdin",
                        "--keep-running",
                        media.url,
                        f"--mpv-force-media-title={media.display_name}",
                    ]

                    if media.referrer is not None:
                        args.append(f"--mpv-referrer={media.referrer}")

                    return subprocess.Popen(args)

                raise errors.PlayerNotSupported(self, self.platform)

            except ModuleNotFoundError:
                raise errors.PlayerNotFound(self)
