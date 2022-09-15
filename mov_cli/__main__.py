import os
import sys
import platform

import click
from .utils.config import config

from .websites.theflix import Theflix
from .websites.actvid import Actvid
from .websites.solar import Solar
from .websites.sflix import Sflix
from .websites.olgply import OlgPly

calls = {
    "actvid": [Actvid, "https://www.actvid.com"],
    "theflix": [Theflix, "https://theflix.to"],
    "sflix": [Sflix, "https://sflix.se"],
    "solar": [Solar, "https://solarmovie.pe"],
    "olgply": [OlgPly, "https://oglply.com"],
}

if platform.system() == "Windows":
    os.system("color FF")  # Fixes colour in Windows 10 CMD terminal.

@click.command()
@click.option(
    "-p",
    "--provider",
    prompt=f"On V:0.1.3\n\n{config.ismac()}\nThe name of the provider",
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
    try:
        provider_data = calls.get(provider, calls["theflix"])
        provider = provider_data[0](provider_data[1])
        # provider.redo(query) if query is not None else provider.redo()
        provider.redo(query, result)  # if result else provider.redo(query)
    except Exception as e:
        print("[!] Sorry I don't know that provider! | ", e)
        sys.exit(2)


if __name__ == '__main__':
    movcli()
