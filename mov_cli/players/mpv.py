import subprocess

from ..utils.player import Player, PlayerNotFound

class Mpv(Player):
    """A class to interface with Mpv cross platform. [Also supports android, OwO!]"""
    def __init__(self, webscraper_class:object) -> None:
        super().__init__("MPV")

        self.__webscraper = webscraper_class
        
    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        
        if self.os == "Android": # Android Support
            print(self.__webscraper.cyan("[!] Detected your using ") + self.__webscraper.green("Android"))

            return subprocess.Popen([
                "am",
                "start",
                "-n",
                "is.xyz.mpv/is.xyz.mpv.MPVActivity",

                "-e",
                "filepath",
                f"{url}",
            ])

        else: # Windows, Linux and Other
            try:
                return subprocess.Popen([
                    "mpv",
                    f"--referrer={referrer}",
                    f"{url}",
                    f"--force-media-title=mov-cli:{media_title}",
                    "--no-terminal",
                ])
            except ModuleNotFoundError:
                raise PlayerNotFound(self)