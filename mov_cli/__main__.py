import os
import sys
import platform

import click
from .utils.provider import ask

from .utils.scraper import WebScraper
from .websites.theflix import Theflix
from .websites.eja import eja
from .websites.kimcartoon import kimcartoon
from .websites.actvid import Actvid
from .websites.dopebox import DopeBox
from .websites.sflix import Sflix
from .websites.solar import Solar
from .websites.viewasian import viewasian
from .websites.gogoanime import gogoanime
from .websites.watchasian import watchasian
from .websites.wlext import wlext
from .websites.streamblasters import streamblasters
from .websites.kinox import kinox
from .websites.hentaimama import hentaimama
from .websites.tamilyogi import tamilyogi
from .websites.javct import javct
from .websites.einthusan import einthusan
from .websites.turkish123 import turkish123

calls = {
    "theflix": [Theflix, "https://theflix.to"],
    "eja" : [eja, "https://eja.tv"],
    "kimcartoon": [kimcartoon, "https://kimcartoon.li"],
    "actvid": [Actvid, "https://www.actvid.com"],
    "sflix": [Sflix, "https://sflix.se"],
    "solar": [Solar, "https://solarmovie.pe"],
    "dopebox": [DopeBox, "https://dopebox.to"],
    "viewasian": [viewasian, "https://viewasian.co"],
    "gogoanime": [gogoanime, "https://www1.gogoanime.bid"],
    "watchasian": [watchasian, "https://watchasian.la"],
    "wlext": [wlext, "https://wlext.is"],
    "streamblasters": [streamblasters, "https://streamblasters.art"],
    "kinox": [kinox, "https://ww17.kinox.to"],
    "hentaimama": [hentaimama, "https://hentaimama.io"],
    "tamilyogi": [tamilyogi, "https://tamilyogi.love"],
    "javct": [javct, "https://javct.net"],
    "einthusan": [einthusan, "https://einthusan.tv"],
    "turkish123": [turkish123, "https://turkish123.ac"],
    }

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal.

def movcli():  # TODO add regex
    provider = ask()
    provider_data = calls.get(provider, calls["actvid"])
    provider:WebScraper = provider_data[0](provider_data[1])
            # provider.redo(query) if query is not None else provider.redo()
    provider.redo()  # if result else provider.redo(query)

if __name__ == '__main__':
    movcli()
