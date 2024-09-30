from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List

    from ..media import Media
    from ..utils.platform import SUPPORTED_PLATFORMS

import subprocess
from devgoldyutils import Colours

from .mpv import MPV

__all__ = ("SyncPlay",)

class SyncPlay(MPV):
    def __init__(
        self, 
        platform: SUPPORTED_PLATFORMS, 
        args: Optional[List[str]] = None, 
        args_override: bool = False, 
        debug: bool = False, 
        **kwargs
    ) -> None:
        super().__init__(
            platform = platform, 
            args = args, 
            debug = debug, 
            args_override = args_override
        )

    @property
    def display_name(self) -> str:
        return Colours.BLUE.apply("Syncplay")

    def play(self, media: Media) -> Optional[subprocess.Popen]:
        """Plays this media in SyncPlay."""
        mpv_args = self._get_args(self.platform, media)

        if self.platform == "Windows" or self.platform == "Linux" or self.platform == "FreeBSD":
            return subprocess.Popen(["syncplay", media.url, "--"] + mpv_args)

        elif self.platform == "Darwin": # NOTE: Limits you to IINA
            default_args = [
                "syncplay", 
                media.url, 
                "--"
            ]

            return subprocess.Popen(
                default_args + [f"--mpv{x.replace('--', '-')}" for x in mpv_args]
            )

        return None