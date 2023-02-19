from fzf import fzf_prompt
from getpass import getuser

english = [
    "actvid",
    "sflix",
    "solar",
    "dopebox",
    "openloadmov",
]

german = [
    "kinox"
]

indian = [
    "streamblasters",
    "tamilyogi",
    "einthusan",
    "wlext",
]

asian = [
    "viewasian",
    "watchasian",
]

anime = [
    "gogoanime",
    "animefox"
]

tv = [
    "eja"
]

cartoons = [
    "kimcartoon"
]

turkish = [
    "turkish123"
]

sports = [
    "scdn"
]

update = [
    "pip install mov-cli"
]

preselction = {
    "English Providers": [english],
    "German Providers": [german],
    "Indian Providers": [indian],
    "Asian Providers": [asian],
    "LIVE TV Providers": [tv],
    "Cartoons Providers": [cartoons],
    "Turkish Providers": [turkish],
    "Anime Providers": [anime],
    "Sports Providers": [sports],
    "": [], f"Hi, {getuser()}" : [],
}

def ask(update: bool = True):
    if update == True:
        preselction.update({"": [], "Update Avaliable!": [update]})
    init = fzf_prompt(preselction)
    get = preselction.get(init)[0]
    choice = fzf_prompt(get)
    return choice


