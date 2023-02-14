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

preselction = [
    "English Providers",
    "German Providers",
    "Indian Providers",
    "Asian Providers",
    "LIVE TV Providers",
    "Cartoons Providers",
    "Turkish Providers",
    "Anime Providers",
]

def ask():
    choice = fzf_prompt(preselction)
    if choice == "English Providers":
        return fzf_prompt(english)
    elif choice == "German Providers":
        return fzf_prompt(german)
    elif choice == "Indian Providers":
        return fzf_prompt(indian)
    elif choice == "Asian Providers":
        return fzf_prompt(asian)
    elif choice == "LIVE TV Providers":
        return fzf_prompt(tv)
    elif choice == "Cartoons Providers":
        return fzf_prompt(cartoons)
    elif choice == "Turkish Providers":
        return fzf_prompt(turkish)
    elif choice == "Anime Providers":
        return fzf_prompt(anime)
    else:
        exit(1)


