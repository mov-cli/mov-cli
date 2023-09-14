import sys
sys.path.insert(0, ".")

import logging
from devgoldyutils import pprint

from mov_cli import mov_cli_logger, Config
from mov_cli.http_client import HTTPClient
from mov_cli.scrapers import Sflix, Eja, Gogoanime, ViewAsian

mov_cli_logger.setLevel(logging.DEBUG)

def show(http_client: HTTPClient):
    rs = ViewAsian(http_client.config, http_client)    
    shows = rs.search("tattooist")
    show = shows[0]
    seasons = show.seasons
    episodes = show.seasons[1]
    pprint((seasons, episodes))
    media = rs.scrape(show, episode=1)
    print(media.url)

def movie(http_client: HTTPClient):
    rs = Sflix(http_client.config, http_client)
    results = rs.search("Hitman Agent 47")
    pprint(results)
    movie = results[0]
    media = rs.scrape(movie)
    print(media.subtitles.get("en"))
    print(media.url)

def tv(http_client: HTTPClient):
    tv = Eja(http_client.config, http_client)
    stations = tv.search("ZDF")
    pprint(stations)
    media = tv.scrape(stations[0])
    print(media.url)

def anime(http_client: HTTPClient):
    gogo = Gogoanime(http_client.config, http_client)
    results = gogo.search("The Pet Girl of Sakurasou")
    pprint(results)
    media = gogo.scrape(results[1], episode = 1)
    print(media.url)


if __name__ == "__main__":
    print("To Test if Movies do work: m, for shows: s, for tv: t, for anime: a")
    a = input("Input: ")

    client = HTTPClient(Config())

    if a.lower() == "m":
        movie(client)
    elif a.lower() == "s":
        show(client)
    elif a.lower() == "a":
        anime(client)
    else:
        tv(client)