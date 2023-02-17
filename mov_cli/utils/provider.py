from fzf import fzf_prompt

english = [
    "actvid",
    "sflix",
    "solar",
    "dopebox",
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
    "sportscentral"
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
}

def ask(update: bool = True):
    if update == True:
        preselction.update({"": [], "Update Avaliable!": [update]})
    init = fzf_prompt(preselction)
    get = preselction.get(init)[0]
    choice = fzf_prompt(get)
    return choice


