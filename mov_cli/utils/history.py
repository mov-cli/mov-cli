import platform
import os
import datetime as dt
class History:
    def __init__(self):
        pass
    @staticmethod
    def winorlinux():
        plt = platform.system()
        if plt == "Windows":
            return f"C://Users//{os.getenv('username')}//Documents"
        elif (plt == "Linux") or (plt == "Darwin"):
            return f"/home/{os.getlogin()}/Documents"
    
    @staticmethod
    def addhistory(name, state, url):
        if state == "d":
            state= "Downloaded"
        else:
            state = "Watched"
        if os.path.exists(f"{History.winorlinux()}//mov_cli"):
            pass
        else:
            os.mkdir(f"{History.winorlinux()}//mov_cli")
        file = f"{History.winorlinux()}//mov_cli//history.txt"
        with open(file, "a") as f:
            f.write(f"{name} | {state} | {url} | {dt.datetime.now()}\n")
    
    @staticmethod
    def gethistory():
        file = f"{History.winorlinux()}//mov_cli//history.txt"
        with open(file, "r") as f:
            history = f.read()
            return print(history)
