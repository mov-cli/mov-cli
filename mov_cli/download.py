from __future__ import annotations
from typing import TYPE_CHECKING
import subprocess
import unicodedata
import os

__all__ = ("Download",)

if TYPE_CHECKING:
    from .config import Config
    from .media import Series, Movie

class Download():
    def __init__(self, config: Config) -> None:
        self.config = config

    def download(self, media: Series | Movie, subtitles: str = None) -> subprocess.Popen:
        title = unicodedata.normalize('NFKD', media.display_name).encode('ascii', 'ignore').decode('ascii') # normalize title
        
        file = os.path.join(self.config.download_location, title + ".mp4")

        args = [
            "ffmpeg",
            "-n",
            "-thread_queue_size",
            "4096",
            "-headers",
            f"Referer: {media.referrer}",
            "-i",
            media.url,
            "-c",
            "copy",
        ]

        if subtitles:
            args.extend(["-vf", f"subtitle={subtitles}"])

        args.append(file)

        return subprocess.Popen(args)
