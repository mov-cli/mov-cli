import os
import platform
from .utils.select import ask
from .utils.scraper import WebScraper
from . import CMD_ARGS

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal


def movcli():  # TODO add regex
    cl, url = ask(CMD_ARGS.p)
    provider: WebScraper = cl.Provider(url)
    provider.redo(CMD_ARGS.s)


if __name__ == "__main__":
    movcli()
