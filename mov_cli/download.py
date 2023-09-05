from __future__ import annotations
from typing import TYPE_CHECKING
import subprocess
import unicodedata

__all__ = ("Download",)

if TYPE_CHECKING:
    from .config import Config
    from .media import Media

class Download():
    def __init__(self, config : Config) -> None:
        super().__init__("Downloader", config)
    
    def dl(self, media : Media, subtitles : str = None):
        title = unicodedata.normalize('NFKD', media.title).encode('ascii', 'ignore').decode('ascii')
        episode = media.episode
        season = media.season
        if episode and season:
            title = title + f"S{season}E{episode}"
        elif episode and season is None:
            title = title + f"E{episode}"
        
        file = Config.dl_location + title + ".mp4"

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
            args.extend(["-vf", f"subtitle={subtitles}", file])
        else:
            args.append(file)
        ffmpeg = subprocess.Popen(args)
        ffmpeg.wait()
        return