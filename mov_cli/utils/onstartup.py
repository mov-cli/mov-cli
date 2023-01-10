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
    def getghkey():
        try:
            with open(f"{startup.winorlinux()}/gh.txt", "r") as f:
                return f.read()
        except: 
            pass

    @staticmethod
    def getkey():
        ghkey = startup.getghkey()
        if ghkey is None:
            dokicloud = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/dokicloud").json()
            rabbitstream = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/rabbitstream").json()
        else:
            dokicloud = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/dokicloud", headers={"Authorization": f"Bearer {ghkey}"}).json()
            rabbitstream = httpx.get("https://api.github.com/repos/consumet/rapidclown/commits/rabbitstream", headers={"Authorization": f"Bearer {ghkey}"}).json()
        dokidate = dokicloud["commit"]["author"]["date"]
        rabbitdate = rabbitstream["commit"]["author"]["date"]
        if dokidate > rabbitdate:
            decryptkey = "https://raw.githubusercontent.com/consumet/rapidclown/dokicloud/key.txt"
        else:
            decryptkey = "https://raw.githubusercontent.com/consumet/rapidclown/rabbitstream/key.txt"
        u = httpx.get(decryptkey).text
        with open(f"{startup.winorlinux()}/movclikey.txt", "w") as f:
            f.write(u)
            