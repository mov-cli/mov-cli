import httpx
from fzf import fzf_prompt
from .props import home
import mov_cli.__main__ as mc
from json import loads
from .props import RestartNeeded, LanguageNotAOption

sel = eval(
    httpx.get("https://raw.githubusercontent.com/mov-cli/translations/main/langs").text
)

def getlang():
    try:
        with open(home() + ".mov_cli_lang", "r") as f:
            lang = f.read()
        existing(lang)
        t = httpx.get(        
            f"https://raw.githubusercontent.com/mov-cli/translations/main/languages/{lang}.json"
        ).json()
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
        import locale
        localLang = locale.getdefaultlocale()[0][:2]
        check = existing(localLang, True)
        if check is True:
            lang = localLang
        else:
            lang = "en"
        with open(home() + ".mov_cli_lang", "w") as f:
            f.write(lang)
        print(f"[?] Your Language was set to {lang}")
        raise RestartNeeded()

def existing(language: str, g = False):
    js = loads(httpx.get("https://raw.githubusercontent.com/mov-cli/translations/main/langs").text)

    exist = False

    if g is False:
        for _, value in js.items():
            if value == language:
                exist = True
        if not exist:    
            raise LanguageNotAOption(language)
    else:
        for _, value in js.items():
            if value == language:
                exist = True
        return exist

def setlang():
    s = fzf_prompt(sel)
    selection = sel.get(s)
    with open(home() + ".mov_cli_lang", "w") as f:
        f.write(selection)