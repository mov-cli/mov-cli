import httpx
import platform as pf
import os
from os import environ
import json
from fzf import fzf_prompt

sel = eval(httpx.get("https://raw.githubusercontent.com/mov-cli/translations/main/langs").text)

def homepath() -> str:
    plt = pf.system()
    if plt == "Windows":
        username = environ["username"]
        return f"C:/Users/{username}/"
    elif (plt == "Linux") or (plt == "Darwin"):
        return f"/home/{os.getlogin()}/"


def getlang():
    try:
        with open(homepath() + "lang.json", "r") as f:
            t = json.load(f)
        ask = t["ASK"]
        ex = t["EXIT"]
        searcha = t["SEARCHA"]
        download = t["DOWNLOAD"]
        spro = t["SPROVIDER"]
        dshow = t["DSHOW"]
        dseason = t["DSEASON"]
        season = t["SEASON"]
        episode = t["EPISODE"]
        change = t["CHANGE"]
        t = [ask, ex, searcha, download, spro, dshow, dseason, season, episode, change]
        return t
    except FileNotFoundError:
        t = httpx.get("https://raw.githubusercontent.com/mov-cli/translations/main/languages/en.json").json()
        ask = t["ASK"]
        ex = t["EXIT"]
        searcha = t["SEARCHA"]
        download = t["DOWNLOAD"]
        spro = t["SPROVIDER"]
        dshow = t["DSHOW"]
        dseason = t["DSEASON"]
        season = t["SEASON"]
        episode = t["EPISODE"]
        change = t["CHANGE"]
        t = [ask, ex, searcha, download, spro, dshow, dseason, season, episode, change]
        return t
    except json.decoder.JSONDecodeError:
        plt = pf.system()
        if plt == "Windows":
            username = environ["username"]
            print(fr"Please delete the lang.json in this directory: C:\Users\{username}")
            exit(0)
        elif (plt == "Linux") or (plt == "Darwin"):
            print(f"Please delete the lang.json in this directory: /home/{os.getlogin()}/") 
            exit(0)

def setlang():
    s = fzf_prompt(sel)
    selection = sel.get(s)
    print(selection)
    txt = httpx.get(f"https://raw.githubusercontent.com/mov-cli/translations/main/languages/{selection}.json").text 
    with open(homepath() + "lang.json", "w") as f:
        f.write(txt)
