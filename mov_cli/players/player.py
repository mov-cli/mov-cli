import sys
import subprocess

from .. import CMD_ARGS
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

            print(
                f"\033]8;;outplayer://{url}\033\\-------------------------\n- Tap to open Outplayer -\n-------------------------\033]8;;\033\\\n"
            )

            sys.exit(1)

        else:  # Windows, Linux and Other
            try:
                if self.os == "Linux" or self.os == "Windows":
                    mpv_args = [
                        f"--referrer={referrer}",
                        f"{url}",
                        f"--force-media-title=mov-cli:{media_title}",
                        "--no-terminal",
                    ]

                    if (
                        CMD_ARGS.flatpak_mpv and self.os == "Linux"
                    ):  # Support for MPV on Flatpak.
                        print("Using flatpak installation of MPV.")
                        return subprocess.Popen(
                            ["flatpak", "run", "io.mpv.Mpv"] + mpv_args
                        )

                    if CMD_ARGS.vlc:
                        vlc_args = [
                            "vlc",
                            f'--http-referrer="{referrer}"',
                            f'"{url}"',
                            f'--meta-title="mov-cli:{media_title}"',
                            "--no-terminal",
                        ]
                        try:
                            return subprocess.Popen(vlc_args)
                        except:
                            raise PlayerNotFound(self)
                    return subprocess.Popen(["mpv"] + mpv_args)

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
                    raise Exception(
                        "[!] Could not determine what Player to use on your OS"
                    )

            except ModuleNotFoundError:
                raise PlayerNotFound(self)
