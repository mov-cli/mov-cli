import os
import subprocess

from ..utils.player import Player, PlayerNotFound

class Mpv(Player):
    """A class to interface with Mpv cross platform. [Also supports android, OwO!]"""
    def __init__(self, webscraper_class:object) -> None:
        super().__init__("MPV")

        self.__webscraper = webscraper_class
        
    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        
        if self.os == "Android": # Android Support
            print(self.__webscraper.cyan("[!] Detected your using ") + self.__webscraper.green("Android."))

            # Change referrer url in custom.conf file. Create a custom.conf file in root directory if it does not exist.
            # -----------------------
            print("owo5")

            # Open file but create if doesn't exist.
            custom_conf_path = f"{os.getenv('HOME')}/storage/shared/custom.conf"
            open(custom_conf_path, "a").close()

            # Rewrite file with new referrer.
            custom_conf_file = open(f"{os.getenv('HOME')}/storage/shared/custom.conf", "w") # I hope this works for everyone. 🙏 #TODO: Test this on different android devices.
            custom_conf_file.seek(0)
            custom_conf_file.write(f'referrer="{referrer}/"')
            custom_conf_file.truncate()

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
                return subprocess.Popen([
                    "mpv",
                    f"--referrer={referrer}",
                    f"{url}",
                    f"--force-media-title=mov-cli:{media_title}",
                    "--no-terminal",
                ])
            except ModuleNotFoundError:
                raise PlayerNotFound(self)