import os
import platform
from .utils.provider import ask
from .utils.scraper import WebScraper

from .websites.eja import eja

# from .websites.kimcartoon import kimcartoon
from .websites.actvid import actvid
from .websites.dopebox import dopebox
from .websites.sflix import sflix
from .websites.solar import solar
from .websites.viewasian import viewasian
from .websites.gogoanime import gogoanime
from .websites.watchasian import watchasian
from .websites.wlext import wlext
from .websites.streamblasters import streamblasters
from .websites.kinox import kinox
from .websites.tamilyogi import tamilyogi
from .websites.einthusan import einthusan
from .websites.turkish123 import turkish123
from .websites.animefox import animefox
from .websites.scdn import scdn
from .websites.openloadmov import openloadmov
from .websites.remotestream import remotestream
from .websites.kisscartoon import kisscartoon
from .websites.yoturkish import yoturkish

calls = {
    "eja": [eja, "https://eja.tv"],
    # "kimcartoon": [kimcartoon, "https://kimcartoon.li"],
    "actvid": [actvid, "https://www.actvid.com"],
    "sflix": [sflix, "https://sflix.se"],
    "solar": [solar, "https://solarmovie.pe"],
    "dopebox": [dopebox, "https://dopebox.to"],
    "viewasian": [viewasian, "https://viewasian.co"],
    "gogoanime": [gogoanime, "https://gogoanime.cl"],
    "watchasian": [watchasian, "https://www1.watchasian.id"],
    "wlext": [wlext, "https://wlext.is"],
    "streamblasters": [streamblasters, "https://streamblasters.pro"],
    "kinox": [kinox, "https://ww17.kinox.to"],
    "tamilyogi": [tamilyogi, "https://tamilyogi.how"],
    "einthusan": [einthusan, "https://einthusan.tv"],
    "turkish123": [turkish123, "https://turkish123.ac"],
    "animefox": [animefox, "https://animefox.to"],
    "scdn": [scdn, ""],
    "openloadmov": [openloadmov, "https://openloadmov.com"],
    "remotestream": [remotestream, "https://remotestre.am"],
    "kisscartoon": [kisscartoon, "https://thekisscartoon.com"],
    "yoturkish": [yoturkish, "https://www1.yoturkish.com"],
}

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal


def movcli():  # TODO add regex
    try:
        provider = ask()
        provider_data = calls.get(provider, calls["actvid"])
        provider: WebScraper = provider_data[0](provider_data[1])
        # provider.redo(query) if query is not None else provider.redo()
        provider.redo()  # if result else provider.redo(query)
    except UnicodeDecodeError:
        print("[!] The Current Key is not correct, please wait.")


if __name__ == "__main__":
    movcli()
