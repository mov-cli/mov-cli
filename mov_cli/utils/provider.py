from fzf import fzf_prompt

english = [
    "theflix",
    "actvid",
    "sflix",
    "solar",
    "dopebox",
    "wlext",
]

german = [
    "kinox"
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

anime = [
    "gogoanime"
]

nsfw = [
    "hentaimama",
    "javct",
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
    "18+ Providers",
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
    elif choice == "18+ Providers":
        return fzf_prompt(nsfw)
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


