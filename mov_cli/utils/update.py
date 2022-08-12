from ..__version__ import __core__
import requests
import sys
import subprocess


class update:
    def __init__(self):
        pass
    @staticmethod
    def checkupdate():
        unformated = requests.get("https://raw.githubusercontent.com/mov-cli/mov-cli/v3/mov_cli/__version__.py").text
        newversion = unformated.split("__core__ = ")[1]
        # strip all dots
        newversion = newversion.replace(".", "")
        localversion = __core__.replace(".", "")
        if newversion == localversion:
            print("No update available")
        else:
            print("[!] New version available! | ", unformated)
            print("[!] You can download it from https://github.com/mov-cli/mov-cli")
            choice = input("[!] Do you want to update? [y/n]: ").lower()
            if choice == "y":
                print("[!] Updating...")
                subprocess.Popen("pip install git+https://github.com/mov-cli/mov-cli")
                sys.exit(1)
            else:
                return


    
