import platform
import os
import datetime as dt
from .dbs import get_imdb_title
from os import environ

class History:
    def __init__(self):
        pass
    @staticmethod
    def winorlinux():
        plt = platform.system()
        if plt == "Windows":
            return f'{environ["USERPROFILE"]}\\Documents'
        elif plt == "Linux":
            return f"/home/{os.getlogin()}"
        elif plt == "Darwin":
            return f"/Users/{os.getlogin()}"
    
    @staticmethod
    def addhistory(userinput, state, url, season=None, episode=None):
        if state == "d":
            state= "Downloaded"
        else:
            state = "Watched"
        if os.path.exists(f"{History.winorlinux()}/mov_cli"):
            pass
        else:
            os.mkdir(f"{History.winorlinux()}/mov_cli")
        file = f"{History.winorlinux()}/mov_cli/history.txt"
        name = get_imdb_title(userinput)
        if season is None:
            pass
        else:
            name = f"{name} - S {season} EP {episode}"
        with open(file, "a") as f:
            f.write(f"{name} | {state} | {url} | {dt.datetime.now()}\n")
    
    @staticmethod
    def gethistory():
        file = f"{History.winorlinux()}/mov_cli/history.txt"
        with open(file, "r") as f:
            history = f.read()
            return print(history)
