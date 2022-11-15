import subprocess

from ..utils.player import Player, PlayerNotFound

class Vlc(Player):
    """A class to interface with VLC. You know, for those VLC users."""
    def __init__(self, webscraper_class:object) -> None:
        super().__init__("VLC")

        self.__webscraper = webscraper_class
        
    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        # No android support yet here like MPV because I'm lazy but I may add it in the future.
        
        try:
            # Windows, Linux and Other
            return subprocess.Popen([
                "vlc",
                f"--http-referrer={referrer}",
                f"{url}",
                f"--meta-title=mov-cli{media_title}",
                "--no-terminal",
            ])

        except ModuleNotFoundError:
            raise PlayerNotFound(self)