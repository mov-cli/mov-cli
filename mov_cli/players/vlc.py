from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List

    from pathlib import Path
    from ..media import Media
    from ..utils.platform import SUPPORTED_PLATFORMS

import httpx
import subprocess
import unicodedata
from devgoldyutils import Colours, LoggerAdapter

from ..logger import mov_cli_logger
from ..utils import get_temp_directory
from ..errors import ReferrerNotSupportedError

from .player import Player

__all__ = ("VLC",)

logger = LoggerAdapter(mov_cli_logger, prefix = Colours.ORANGE.apply("VLC"))

class VLC(Player):
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
        return Colours.ORANGE.apply("VLC")

    def play(self, media: Media) -> Optional[subprocess.Popen]:
        """Plays this media in the VLC media player."""

        if self.platform == "Android":

            if media.referrer is not None:
                raise ReferrerNotSupportedError(
                    "The VLC player on Android does not support passing referrers, so this media cannot be played. :("
                )

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

            if media.referrer is not None:
                raise ReferrerNotSupportedError(
                    "The VLC player on iOS does not support passing referrers, so this media cannot be played. :("
                )

            with open('/dev/clipboard', 'w') as f:
                f.write(f"vlc://{media.url}")

            logger.info("The URL was copied into your clipboard. To play it, open a browser and paste the URL.")

            return None

        elif self.platform == "Linux" or self.platform == "Windows" or self.platform == "FreeBSD":
            default_args = [
                "vlc", 
                media.url
            ]

            if media.audio_tracks is not None:
                default_args.append(f"--input-slave={media.audio_tracks[0].url}") # WHY IS THIS UNDOCUMENTED!!!

            args = [
                f'--meta-title="{media.display_name}"'
            ]

            if media.referrer is not None:
                args.append(f'--http-referrer="{media.referrer}"')

            if media.subtitles is not None:

                for subtitle in media.subtitles:

                    if subtitle.startswith("https://"):
                        logger.debug("Subtitles detected as a url.")
                        subtitle = str(self.__url_subtitles_to_file(media, subtitle.url))

                    args.append(f"--sub-file={subtitle}")

            if self.debug is False:
                args.append("--quiet")

            args = self.handle_additional_args(args, self.args)

            return subprocess.Popen(default_args + args)

        return None

    def __url_subtitles_to_file(self, media: Media, subtitles_url: str) -> Path:
        sub_file_exists_already = False
        temp_dir = get_temp_directory(self.platform)

        file_name = unicodedata.normalize("NFKD", media.display_name).encode("ascii", "ignore").decode("ascii")
        file_path = temp_dir.joinpath(file_name)

        if file_path.exists():
            sub_file_exists_already = True
            logger.debug("Subtitles already exists in temp directory, skipping download...")

        if sub_file_exists_already is False:
            logger.debug("Downloading subtitles to temp directory as vlc does not support streaming of subs via url...")
            response = httpx.get(url = subtitles_url)

            with file_path.open("wb") as file:
                file.write(response.content)

        return file_path