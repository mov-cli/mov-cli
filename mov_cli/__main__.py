import os
import sys
import platform

import click
from .utils.config import config

from .websites.theflix import Theflix
from .websites.vidsrc import Vidsrc
from .websites.eja import eja
from .websites.trailers import trailers
from .websites.ask4movie import Ask4Movie
from .websites.ustvgo import ustvgo
from .websites.kimcartoon import kimcartoon

calls = {
    "theflix": [Theflix, "https://theflix.to"],
    "vidsrc": [Vidsrc, "https://v2.vidsrc.me"],
    "eja" : [eja, "https://eja.tv"],
    "trailers": [trailers, "https://trailers.to"],
    "ask4movie": [Ask4Movie, "https://ask4movie.mx"],
    "ustvgo": [ustvgo, "https://ustvgo.tv"],
    "kimcartoon": [kimcartoon, "https://kimcartoon.li"],
}

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal.

@click.command()
@click.option(
    "-p",
    "--provider",
    prompt=f"\ntheflix\nvidsrc\neja\nask4movie\nustvgo / US IP ONLY\nkimcartoon\n\nThe name of the provider",
    help='The name of the provider ex: "theflix"',
    default=f"{config.getprovider()}",
)
@click.option("-q", "--query", default=None, help="Your search query")
@click.option(
    "-r",
    "--result",
    default=None,
    help="The Result Number you want to be played",
    type=int,
)
def movcli(provider, query, result):  # TODO add regex
    provider_data = calls.get(provider, calls["theflix"])
    provider = provider_data[0](provider_data[1])
        # provider.redo(query) if query is not None else provider.redo()
    provider.redo(query, result)  # if result else provider.redo(query)


if __name__ == '__main__':
    movcli()
