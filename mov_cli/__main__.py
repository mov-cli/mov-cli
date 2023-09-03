import os
import platform
from .utils.select import ask
from .utils.scraper import WebScraper
from . import CMD_ARGS

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal

def __process_args():
    arg_p = CMD_ARGS.p
    arg_s = CMD_ARGS.s
    CMD_ARGS.s = None
    CMD_ARGS.p = None
    return arg_p, arg_s

def movcli():  # TODO add regex
    p, s = __process_args()
    cl, url = ask(p)
    provider: WebScraper = cl.Provider(url)
    provider.redo(s)


if __name__ == "__main__":
    movcli()
