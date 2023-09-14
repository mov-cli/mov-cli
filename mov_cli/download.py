from __future__ import annotations
from typing import TYPE_CHECKING
import subprocess
import unicodedata

__all__ = ("Download",)

if TYPE_CHECKING:
    from .config import Config
    from .media import LiveTV, Series, Movie

class Download():
    def __init__(self, config: Config) -> None:
        self.config = config

    def download(self, media: LiveTV | Series | Movie, subtitles: str = None):
        title = unicodedata.normalize('NFKD', media.title).encode('ascii', 'ignore').decode('ascii')
        episode = media.episode
        season = media.season

        if season is not None:
            title += f" S{season}"

        if episode is not None:
            title += f" E{episode}"

        file = self.config.download_location + title + ".mp4"

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

        try:
            ffmpeg = subprocess.Popen(args)
            ffmpeg.wait()
            return True
        except Exception:
            return False 