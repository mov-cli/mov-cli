import sys
import subprocess
import time


from ..utils.player import Player, PlayerNotFound


class ply(Player):
    """A class to start the Player."""

    def __init__(self, webscraper_class: object) -> None:
        super().__init__("PlAYER")

        self.webscraper = webscraper_class

    def play(self, url: str, referrer: str, media_title: str) -> subprocess.Popen:
        if self.os == "Android":  # Android Support
            print("[!] Detected your using Android.")

            return subprocess.Popen(
                [
                    "am",
                    "start",
                    "-n",
                    "is.xyz.mpv/is.xyz.mpv.MPVActivity",
                    "-e",
                    "filepath",
                    f"{url}",
                ]
            )
    
        elif self.os == "iOS":
            print("[!] Detected your using iOS. \r\n")
            
            print(f'\033]8;;outplayer://{url}\033\\-------------------------\n- Tap to open Outplayer -\n-------------------------\033]8;;\033\\\n')

            sys.exit(1)

        else:  # Windows, Linux and Other
            try:
                if self.os == "Linux" or self.os == "Windows":
                    return subprocess.Popen(
                        [
                            "mpv",
                            f"--referrer={referrer}",
                            f"{url}",
                            f"--force-media-title=mov-cli:{media_title}",
                            "--no-terminal",
                        ]
                    )

                elif self.os == "Darwin":
                    return subprocess.Popen(
                        [
                            "iina",
                            "--no-stdin",
                            "--keep-running",
                            f"--mpv-referrer={referrer}",
                            url,
                            f"--mpv-force-media-title=mov-cli:{media_title}",
                        ]
                    )

                else:
                    print("[!] Could not determine what Player to use on your OS")
                    sys.exit(1)

            except ModuleNotFoundError:
                raise PlayerNotFound(self)
