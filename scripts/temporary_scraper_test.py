from mov_cli.config import Config
from mov_cli.scrapers import Sflix, SolarMovies, RemoteStream, eja, Turkish123, gogoanime, ViewAsian
import logging
from mov_cli import mov_cli_logger
from devgoldyutils import pprint

mov_cli_logger.setLevel(logging.DEBUG)
def show():
    rs = ViewAsian(Config())    
    shows = rs.search("tattooist")
    show = shows[0]
    seasons = show.seasons
    episodes = show.seasons[1]
    pprint((seasons, episodes))
    media = rs.scrape(show, episode=1)
    print(media.url)

def movie():
    rs = Sflix(Config())
    results = rs.search("Hitman Agent 47")
    pprint(results)
    movie = results[0]
    media = rs.scrape(movie)
    print(media.subtitles.get("en"))
    print(media.url)

def tv():
    tv = eja(Config())
    stations = tv.search("ZDF")
    pprint(stations)
    media = tv.scrape(stations[0])
    print(media.url)

def anime():
    gogo = gogoanime(Config())
    results = gogo.search("The Pet Girl of Sakurasou")
    pprint(results)
    media = gogo.scrape(results[1], episode = 1)
    print(media.url)


if __name__ == "__main__":
    print("To Test if Movies do work: m, for shows: s, for tv: t, for anime: a")
    a = input("Input: ")
    if a.lower() == "m":
        movie()
    elif a.lower() == "s":
        show()
    elif a.lower() == "a":
        anime()
    else:
        tv()