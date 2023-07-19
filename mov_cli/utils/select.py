from fzf import fzf_prompt
from importlib import import_module
from .. import CMD_ARGS
from argparse import ArgumentError


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
}


preselction = {
    "English Providers": [english],
    "Indian Providers": [indian],
    "Asian Providers": [asian],
    "LIVETV Providers": [tv],
    "Cartoons Providers": [cartoons],
    "Turkish Providers": [turkish],
    "Anime Providers": [anime],
    "Sports Providers": [sports],
    "International Providers": [inter],
}

calls = {
    "eja": "https://eja.tv",
    "actvid": "https://actvid.rs",
    "sflix": "https://sflix.se",
    "solar": "https://solarmovie.pe",
    "dopebox": "https://dopebox.to",
    "viewasian": "https://viewasian.co",
    "gogoanime": "https://gogoanime.hu",
    "watchasian": "https://watchasian.mx",
    "wlext": "https://wlext.is",
    "streamblasters": "https://streamblasters.pro",
    "tamilyogi": "https://tamilyogi.bike",
    "einthusan": "https://einthusan.tv",
    "turkish123": "https://turkish123.ac",
    "scdn": "",
    "remotestream": "https://remotestre.am",
    "kisscartoon": "https://thekisscartoon.com",
    "yoturkish": "https://www1.yoturkish.com",
}


def export(provider: str, typ: str):
    module = f"mov_cli.websites.{typ}.{provider}"
    return import_module(module)


def ask(provider: str = None):
    if provider:
        provider = provider.replace(" ", "")
        get = calls.get(provider)
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
            cl = export(provider, typ)
            return cl, get
    else:
        init = fzf_prompt(preselction)
        get = preselction.get(init)[0]
        choice = fzf_prompt(get)
        typ = init.split(" ")[0].lower()
        cl = export(choice, typ)
        return cl, calls.get(choice)
