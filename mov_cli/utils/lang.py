from fzf import fzf_prompt
from .props import home
import mov_cli.__main__ as mc
from json import loads
from .props import LanguageNotAOption
from pkgutil import get_data

langsfile = get_data(__name__, "lang/langs")

langsfile = loads(langsfile)

def existing(language: str, g: bool = False):

    exist = False

    for _, value in langsfile.items():
        if value == language:
            exist = True
    if not exist and not g:
        raise LanguageNotAOption(language)
    else:
        return exist

def getlang():
    try:
        with open(f"{home()}/lang.mov-cli", "r") as f:
            lang = f.read()
        existing(lang)
        t = loads(get_data(__name__, f"lang/{lang}.json"))
        items = []
        for _, value in t.items():
            items.append(value)
        return items
    except FileNotFoundError:
        import locale

        localLang = locale.getdefaultlocale()[0][:2]
        check = existing(localLang, True)
        if check:
            lang = localLang
        else:
            lang = "en"
        open(f"{home()}/lang.mov-cli", "w").write(lang)
        return mc.movcli()

def setlang():
    s = fzf_prompt(langsfile)
    selection = langsfile.get(s)
    open(f"{home()}/lang.mov-cli", "w").write(selection)