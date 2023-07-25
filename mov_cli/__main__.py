import os
import platform
from .utils.select import ask
from .utils.scraper import WebScraper
from . import CMD_ARGS

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal


def movcli():  # TODO add regex
    if CMD_ARGS.debug:
        cl, url = ask(CMD_ARGS.p)
        provider: WebScraper = cl.Provider(url)
        provider.redo(CMD_ARGS.s)
    else:
        try:
            cl, url = ask(CMD_ARGS.p)
            provider: WebScraper = cl.Provider(url)
            provider.redo(CMD_ARGS.s)
        except UnicodeDecodeError:
            print("[!] The Current Key is not correct, please wait.")
        except Exception as e:
            print(f"[!] An Exception has occurred | {e}")


if __name__ == "__main__":
    movcli()
