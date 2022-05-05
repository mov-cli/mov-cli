import sys

import click

from .websites.theflix import Theflix
from .websites.actvid import Actvid
from .websites.solar import Solar
from .websites.sflix import Sflix

calls = {
    'actvid': Actvid,
    'theflix': Theflix,
    'sflix': Sflix,
    'solar': Solar
}

@click.command()
    # @click.option('--name', prompt='The name of the movie/series with the provider',
    #              help='The name of the movie/series with the provide, ex: "theflix;friends"')
    # TODO doesn't work fully yet
    # @click.option('--regex', default=None, help='allows you to apply regexes to the search queries')
def main():  # TODO add regex
    name = input("Please name the movie/series with the provider, ex: theflix: ").lower()
        # name, query = name.replace("'", '').replace('"', '').split(';')
    if name == "actvid":
        provider = calls[name]('https://www.actvid.com')
        provider.redo()
    elif name == 'theflix':
        provider = calls[name]('https://theflix.to')
        provider.redo()
    elif name == 'sflix':
        provider = calls[name]('https://sflix.se')
        provider.redo()
    elif name == 'solar':
        provider = calls[name]('https://solarmovie.pe')
        provider.redo()
    else:
        print("Sorry, I don't know that provider")
        sys.exit(-2)


#if __name__ == '__main__':
#    main()