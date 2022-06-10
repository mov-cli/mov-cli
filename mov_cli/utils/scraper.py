import re
import os
import sys
import logging
import platform

from .httpclient import HttpClient
from colorama import Fore, Style


def determine_path() -> str:
    plt = platform.system()
    if plt == "Windows":
        return f"C://Users//{os.getenv('username')}//Downloads"
    elif (plt == "Linux") or (plt == "Darwin"):
        return r"~/Downloads"
    else:
        print("Please open an issue for your os")
        sys.exit(-2)


class WebScraper:
    def __init__(self, base_url) -> None:
        self.client = HttpClient()
        self.base_url = base_url
        pass

    def blue(self, txt: str) -> str:
        return f"{Fore.BLUE}{txt}{Style.RESET_ALL}"

    def yellow(self, txt: str) -> str:
        return f"{Fore.YELLOW}{txt}{Style.RESET_ALL}"

    def red(self, txt: str) -> str:
        return f"{Fore.RED}{txt}{Style.RESET_ALL}"

    def lmagenta(self, txt: str) -> str:
        return f"{Fore.LIGHTMAGENTA_EX}{txt}{Style.RESET_ALL}"

    def cyan(self, txt: str) -> str:
        return f"{Fore.CYAN}{txt}{Style.RESET_ALL}"

    def green(self, txt: str) -> str:
        return f"{Fore.GREEN}{txt}{Style.RESET_ALL}"

    def parse(self, txt: str) -> str:
        return re.sub("\W+", "-", txt.lower())

    def search(self, q: str = None) -> str:
        return NotImplementedError()

    def results(self, data: str) -> list:
        return NotImplementedError()

    def dl(
        self, url: str, name: str, path: str = determine_path(), subtitle: str = None
    ):  # "./"
        if not subtitle:
            os.system(
                f'ffmpeg -loglevel error -stats -i "{url}" -c copy {path}/{name}.mp4'
            )
            return print(self.blue(f"Downloaded {name} at {path}"))
        os.system(
            f'ffmpeg -loglevel error -stats -i "{url}" -i {subtitle} -c copy -c:s mov_text"{path}/{name}.mp4"'
        )
        # ! The subtitles are not synced with the video
        return print(self.blue(f"Downloaded {name} at {path}"))

    def play(self, url: str, name: str):
        try:
            try:
                os.system(
                    f'mpv --referrer="{self.base_url}" "{url}" --force-media-title="mov-cli:{name}"'
                )
            except ModuleNotFoundError:  ##why do you even exist if you don't have MPV installed? WHY?
                os.system(
                    f'vlc --http-referrer="{self.base_url}" "{url}" --meta-title="mov-cli{name}"'
                )
        except Exception as e:
            txt = f"{self.red('[!]')} Could not play {name}: MPV or VLC not found | {e}"
            logging.log(logging.ERROR, txt)
            # print(txt)  # TODO implement logging to a file
            sys.exit(1)
