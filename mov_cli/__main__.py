import os
import platform
from .utils.provider import ask
from .utils.scraper import WebScraper
from .utils.props import RestartNeeded, LanguageNotAOption

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal

def movcli():  # TODO add regex
    try:
        cl, url = ask()
        provider: WebScraper = cl.Provider(url)
        # provider.redo(query) if query is not None else provider.redo()
        provider.redo()  # if result else provider.redo(query)
    except UnicodeDecodeError:
        print("[!] The Current Key is not correct, please wait.")
    except Exception as e:
        print(f"[!] An Exception has occurred | {e}")
    except LanguageNotAOption:
        pass
    except RestartNeeded:
        pass

if __name__ == "__main__":
    movcli()