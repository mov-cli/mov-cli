from fzf import fzf_prompt
from importlib import import_module
from .props import home, RestartNeeded
from httpx import get
import json
from .props import firstStart

base = {
    "eja": "https://eja.tv",
    "sflix": "https://sflix.se",
    "solar": "https://solarmovie.pe",
    "dopebox": "https://dopebox.to",
    "viewasian": "https://viewasian.co",
    "gogoanime": "https://gogoanimehd.io",
    "watchasian": "https://watchasian.mx",
    "wlext": "https://wlext.is",
    "streamblasters": "https://streamblasters.pics",
    "tamilyogi": "https://tamilyogi.band",
    "einthusan": "https://einthusan.tv",
    "turkish123": "https://turkish123.ac",
    "scdn": "",
    "remotestream": "https://remotestre.am",
    "kisscartoon": "https://thekisscartoon.com",
    "yoturkish": "https://www1.yoturkish.com",
}

english = ["sflix", "solar", "dopebox", "remotestream"] # actvid is not using dokicloud

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
    firstStart()
    try:
        js = open(f"{home()}/provider.mov-cli")
        calls = json.load(js)
    except FileNotFoundError:
        with open(f"{home()}/provider.mov-cli", "w") as f:
            f.write(json.dumps(base))
        raise RestartNeeded
    except json.decoder.JSONDecodeError:
        with open(f"{home()}/provider.mov-cli", "w") as f:
            f.write(json.dumps(base))
        raise RestartNeeded
    try:
        from porn_cli.__main__ import websites

        if ph != []:
            return dict(calls)
        for main, sub in websites.items():
            calls[main] = sub
            ph.append(str(main))
            preselction["Porn Providers"] = ph
        return dict(calls)
    except:
        return dict(calls)


def ask(provider: str = None):
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
        if init is None:
            exit(1)
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
    import tldextract

    DEFAULT_HEADERS: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.163 "
        "Safari/537.36",
        "Accept-Language": "en-GB,en;q=0.5",
    }

    calls = json.loads(open(f"{home()}/provider.mov-cli").read())
    for main, sub in dict(calls).items():
        if sub == "":
            continue
        try:
            check = get(sub, follow_redirects=True, headers=DEFAULT_HEADERS, timeout=10)
        except:
            continue
        checkext = tldextract.extract(str(check.url))
        subext = tldextract.extract(sub)
        if checkext.registered_domain == subext.registered_domain:
            print(f"Checked: {main}")
        else:
            if checkext.subdomain:
                updatedurl = (
                    "https://" + checkext.subdomain + "." + checkext.registered_domain
                )
            else:
                updatedurl = "https://" + checkext.registered_domain
            calls[main] = updatedurl
            print(f"Updated: {main} from {sub} to {updatedurl}")
    open(f"{home()}/provider.mov-cli", "w").write(json.dumps(calls))
    print("Provider Check: Done")
    exit(0)
