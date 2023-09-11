from mov_cli.config import Config
from mov_cli.scrapers import DopeBox, Sflix, SolarMovies, RemoteStream, eja
from devgoldyutils import pprint

def show():
    rs = SolarMovies(Config())    
    shows = rs.search("Prison Break")
    show = shows[1]
    seasons = show.seasons
    episodes = show.seasons[1]
    pprint((seasons, episodes))
    media = rs.scrape(show, 1, 1)
    print(media.subtitles.get("en"))
    pprint(media.url)

def movie():
    rs = DopeBox(Config())
    results = rs.search("Hitman Agent 47")
    pprint(results)
    movie = results[0]
    media = rs.scrape(movie)
    print(media.subtitles.get("en"))
    pprint(media.url)

def tv():
    tv = eja(Config())
    stations = tv.search("ZDF")
    pprint(stations)
    media = tv.scrape(stations[0])
    pprint(media.url)

if __name__ == "__main__":
    print("To Test if Movies do work: m, for shows: s, for tv: t")
    a = input("Input: ")
    if a.lower() == "m":
        movie()
    elif a.lower() == "s":
        show()
    else:
        tv()
    