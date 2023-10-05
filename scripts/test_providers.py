from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..mov_cli.scraper import Scraper

import sys
sys.path.insert(0, ".")

import logging
from devgoldyutils import pprint

from mov_cli import mov_cli_logger, Config
from mov_cli.http_client import HTTPClient
from mov_cli.scrapers import Sflix, Eja, Gogoanime, ViewAsian, Turkish123, SolarMovies


mov_cli_logger.setLevel(logging.DEBUG)

# viewasian

asian = [ViewAsian]

asian_query = "tattooist"

# show and movie

mov_show = [Sflix, SolarMovies]

movie_query = "Hitman Agent 47"

show_query = "Prison Break"

# LIVETV

livetv = [Eja]

livetv_query = "ZDF"

# Anime

anime = [Gogoanime]

anime_query = "The Pet Girl of Sakurasou"

# Turkish123

turkish = [Turkish123]

turkish_query = "Sen Cal Kapimi"


def test(http_client: HTTPClient):
    test_js = {}

    for asian_provider in asian:
        provider = asian_provider(http_client.config, http_client)

        search = provider.search(asian_query, 5)[0]

        media = provider.scrape(search, 1)
        test_js[asian_provider.__name__] = {"stream_url": media.url, "q": asian_query, "page_url": search.url}
    
    for livetv_provider in livetv:
        provider = livetv_provider(http_client.config, http_client)

        search = provider.search(livetv_query, 5)[0]

        media = provider.scrape(search)

        test_js[provider.__class__.__name__] = {"stream_url": media.url, "q": livetv_query, "page_url": search.url}
    
    for eng_provider in mov_show:
        provider = eng_provider(http_client.config, http_client)

        provider: Scraper
        
        movie_search = provider.search(movie_query, 5)[0]

        movie_media = provider.scrape(movie_search, 1)

        show_search = provider.search(show_query, 5)[1]

        show_media = provider.scrape(show_search, 1, 1)

        test_js["mov_show"] = {}

        test_js["mov_show"][provider.__class__.__name__] = {"movie": {"stream_url": movie_media.url, "q": movie_query, "page_url": movie_search.url}, 
                                                "show": {"stream_url": show_media.url, "q": show_query, "page_url": show_search.url}}

    for anime_provider in anime:
        provider = anime_provider(http_client.config, http_client)
        
        search = provider.search(anime_query, 5)[0]

        media = provider.scrape(search, 1)

        test_js[provider.__class__.__name__] = {"stream_url": media.url, "q": livetv_query, "page_url": search.url}

    for turkish_provider in turkish:
        provider = turkish_provider(http_client.config, http_client)
        
        search = provider.search(turkish_query, 5)[0]

        media = provider.scrape(search, 1)

        test_js[provider.__class__.__name__] = {"stream_url": media.url, "q": turkish_query, "page_url": search.url}

    pprint(test_js)






if __name__ == "__main__":
    print("Testing Provider")

    client = HTTPClient(Config())

    test(client)
