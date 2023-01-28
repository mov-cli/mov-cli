import sys
import subprocess

from ..utils.player import Player, PlayerNotFound

class Vlc(Player):
    """A class to interface with VLC. You know, for those VLC users."""
    def __init__(self, webscraper_class:object) -> None:
        super().__init__("VLC")

        self.__webscraper = webscraper_class
        
    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        # No android support yet here like MPV because I'm lazy but I may add it in the future if even possible.
        
        try:
            # Windows, Linux and Other

            if self.os == "Linux" or self.os == "Windows":

                return subprocess.Popen([
                    "mpv",
                    f"--referrer={referrer}",
                    f"{url}",
                    f"--force-media-title=mov-cli:{media_title}",
                    "--no-terminal",
                ])

            elif self.os == "Darwin":

                return subprocess.Popen([
                    "iina",
                    "--no-stdin",
                    "--keep-running",
                    f"--mpv-referrer={referrer}",
                    url,
                    f"--mpv-force-media-title=mov-cli:{media_title}"
                ])

            else:
                print(self.red("[!] Could not determine what Player to use on your OS"))
                sys.exit(1)

        except ModuleNotFoundError:
            raise PlayerNotFound(self)