from fzf import fzf_prompt
from importlib import import_module

english = [
    "actvid", 
    "sflix", 
    "solar", 
    "dopebox", 
    "openloadmov", 
    "remotestream"
]

indian = [
    "streamblasters",
    "tamilyogi",
    "einthusan",
]

asian = [
    "viewasian",
    "watchasian",
]

anime = ["gogoanime", "animefox"]

tv = ["eja"]

cartoons = ["kisscartoon"]

turkish = ["turkish123", "yoturkish"]

sports = ["scdn"]

inter = [
    "wlext",
]

preselction = {
    "English Providers": [english],
    "Indian Providers": [indian],
    "Asian Providers": [asian],
    "LIVE TV Providers": [tv],
    "Cartoons Providers": [cartoons],
    "Turkish Providers": [turkish],
    "Anime Providers": [anime],
    "Sports Providers": [sports],
    "International Providers": [inter],
}

calls = {
    "eja": "https://eja.tv",
    # "kimcartoon": [kimcartoon, "https://kimcartoon.li"],
    "actvid": "https://www.actvid.com",
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
    "animefox": "https://animefox.to",
    "scdn": "",
    "openloadmov": "https://openloadmov.com",
    "remotestream": "https://remotestre.am",
    "kisscartoon": "https://thekisscartoon.com",
    "yoturkish": "https://www1.yoturkish.com",
}

def export(provider: str):
    module = f"mov_cli.websites.{provider}"
    return import_module(module)

def ask():
    init = fzf_prompt(preselction)
    get = preselction.get(init)[0]
    choice = fzf_prompt(get)
    cl = export(choice)
    return cl, calls.get(choice)
