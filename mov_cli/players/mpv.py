import os
import sys
import subprocess

from ..utils.player import Player, PlayerNotFound

class Mpv(Player):
    """A class to interface with Mpv cross platform. [Also supports android, OwO!]"""
    def __init__(self, webscraper_class:object) -> None:
        super().__init__("MPV")

        self.webscraper = webscraper_class
        
    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        if self.os == "Android": # Android Support
            print("[!] Detected your using Android.")

            #if "theflix" in url:
            #    raise Exception(self.webscraper.red("'theflix' is not supported on ") + self.webscraper.green("Android!")) as theflix is removed its not required


            # Now open mpv with url.
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
                    print("[!] Could not determine what Player to use on your OS")
                    sys.exit(1)

            except ModuleNotFoundError:
                raise PlayerNotFound(self)