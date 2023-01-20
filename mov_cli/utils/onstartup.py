import httpx
import platform
import getpass
from os import environ
import re

class startup:
    def __init__(self):
        pass

    @staticmethod
    def winorlinux():
        plt = platform.system()
        if plt == "Windows":
            return f'{environ["USERPROFILE"]}'
        elif plt == "Linux":
            return f"/home/{getpass.getuser()}"
        elif plt == "Darwin":
            return f"/Users/{getpass.getuser()}"
        
    @staticmethod
    def getkey():
        key = httpx.get("https://raw.githubusercontent.com/mov-cli/movkey/main/key.txt").text
        with open(f"{startup.winorlinux()}/movclikey.txt", "w") as f:
            f.write(key)
