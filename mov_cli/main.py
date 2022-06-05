import os
import sys
import platform

import click

from .websites.theflix import Theflix
from .websites.actvid import Actvid
from .websites.solar import Solar
from .websites.sflix import Sflix
from .websites.olgply import OlgPly

calls = {
    'actvid': [Actvid, 'https://www.actvid.com'],
    'theflix': [Theflix, 'https://theflix.to'],
    'sflix': [Sflix, 'https://sflix.se'],
    'solar': [Solar, 'https://solarmovie.pe'],
    'olgply': [OlgPly, 'https://oglply.com'],
}
# write a function to get the current platform
if platform.system() == 'Windows':
    os.system('color FF')  # Fixes colour in Windows 10 CMD terminal.


@click.command()
# @click.option('--name', prompt='The name of the movie/series with the provider',
#              help='The name of the movie/series with the provide, ex: "theflix;friends"')
# TODO doesn't work fully yet
# @click.option('--regex', default=None, help='allows you to apply regexes to the search queries')
def main():  # TODO add regex
    name = input("Please name the movie/series with the provider, ex: theflix: ").lower()
    # name, query = name.replace("'", '').replace('"', '').split(';')
    try:
        provider_data = calls[name]
        provider = provider_data[0](provider_data[1])
        provider.redo()
    except KeyError:
        print("[!] Sorry I don't know that provider!")
        sys.exit(2)

# if __name__ == '__main__':
#    main()
