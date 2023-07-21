from fzf import fzf_prompt
from importlib import import_module
from .props import home, RestartNeeded
from httpx import get
import json

english = ["actvid", "sflix", "solar", "dopebox", "remotestream"]

indian = [
    "tamilyogi",
    "einthusan",
    "streamblasters",
]

asian = [
    "viewasian",
    "watchasian",
]

anime = ["gogoanime"]

tv = ["eja"]

cartoons = ["kisscartoon"]

turkish = ["turkish123", "yoturkish"]


sports = ["scdn"]

inter = [
    "wlext",
]

ph = []

ep = {
    "english": english,
    "indian": indian,
    "asian": asian,
    "anime": anime,
    "livetv": tv,
    "cartoons": cartoons,
    "turkish": turkish,
    "sports": sports,
    "international": inter,
    "porn": ph,
}


preselction = {
    "English Providers": english,
    "Indian Providers": indian,
    "Asian Providers": asian,
    "LIVETV Providers": tv,
    "Cartoons Providers": cartoons,
    "Turkish Providers": turkish,
    "Anime Providers": anime,
    "Sports Providers": sports,
    "International Providers": inter,
}


def export(provider: str, typ: str, version: str = "mov_cli"):
    module = f"{version}.websites.{typ}.{provider}"
    return import_module(module)


def p():
    try:
        js = open(f"{home()}/provider.mov-cli")
        calls = json.load(js)
    except FileNotFoundError:
        online = get("https://raw.githubusercontent.com/mov-cli/provider.mov-cli/main/provider.mov-cli").text
        open(f"{home()}/provider.mov-cli", "w").write(online)
        raise RestartNeeded

    from porn_cli.__main__ import websites
    if ph != []:
        return dict(calls)
    for main, sub in websites.items():
        calls[main] = sub
        ph.append(str(main))
        preselction["Porn Providers"] = ph
    return dict(calls)



def ask(provider: str = None):
    updateProvider()
    calls = p()
    if provider:
        provider = provider.replace(" ", "")
        get = calls.get(provider)
        print(get)
        if get is None:
            raise Exception("-p: No such provider was found")
        else:
            typ = ""
            for main, sub in ep.items():
                try:
                    sub.index(provider)
                    typ = main
                    break
                except ValueError:
                    continue
            if typ.__contains__("porn"):
                version = "porn_cli"
            else:
                version = "mov_cli"
            cl = export(provider, typ, version)
            return cl, get
    else:
        init = fzf_prompt(preselction, header="Select:")
        if init is None: exit(1)
        get = preselction.get(init)
        choice = fzf_prompt(get, header="Select:")
        typ = init.split(" ")[0].lower()
        if typ.__contains__("porn"):
            version = "porn_cli"
        else:
            version = "mov_cli"
        cl = export(choice, typ, version)
        return cl, calls.get(choice)


def updateProvider():
    from filecmp import cmp

    online = get(
        "https://raw.githubusercontent.com/mov-cli/provider.mov-cli/main/provider.mov-cli"
    ).text
    open(f"{home()}/provider.mov-cli_temp", "w").write(online)
    check = cmp(f"{home()}/provider.mov-cli", f"{home()}/provider.mov-cli_temp")
    if check:
        from os import remove

        remove(f"{home()}/provider.mov-cli_temp")
    else:

        from os import rename, remove

        remove(f"{home()}/provider.mov-cli")
        rename(f"{home()}/provider.mov-cli_temp", f"{home()}/provider.mov-cli")