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

__all__ = ("MPV",)

logger = LoggerAdapter(mov_cli_logger, prefix = Colours.PURPLE.apply("MPV"))

class MPV(Player):
    def __init__(self, platform: SUPPORTED_PLATFORMS, **kwargs) -> None:
        self.platform = platform

        super().__init__(**kwargs)

    def play(self, media: Media) -> Optional[subprocess.Popen]:
        """Plays this media in the MPV media player."""

        logger.info("Launching MPV Media Player...")

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

        except ModuleNotFoundError:
            raise errors.PlayerNotFound(self)

        return None