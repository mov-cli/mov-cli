import httpx
import platform
import os
from os import environ

class startup:
    def __init__(self):
        pass

    @staticmethod
    def winorlinux():
        plt = platform.system()
        if plt == "Windows":
            return f'{environ["USERPROFILE"]}'
        elif plt == "Linux":
            return f"/home/{os.getlogin()}"
        elif plt == "Darwin":
            return f"/Users/{os.getlogin()}"
    
    @staticmethod
    def getkey():
        dokicloud = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/dokicloud").json()
        rabbitstream = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/rabbitstream").json()
        dokidate = dokicloud["commit"]["author"]["date"]
        rabbitdate = rabbitstream["commit"]["author"]["date"]
        if dokidate > rabbitdate:
            decryptkey = "https://raw.githubusercontent.com/consumet/rapidclown/dokicloud/key.txt"
        else:
            decryptkey = "https://raw.githubusercontent.com/consumet/rapidclown/rabbitstream/key.txt"
        u = httpx.get(decryptkey).text
        with open(f"{startup.winorlinux()}/movclikey.txt", "w") as f:
            f.write(u)
            