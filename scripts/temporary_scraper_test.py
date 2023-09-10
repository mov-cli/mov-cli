from mov_cli.config import Config
from mov_cli.scrapers import DopeBox, Sflix, RemoteStream

def show():
    rs = Sflix(Config())
    shows = rs.search("The Grand Tour")
    print(shows)
    show = shows[0]
    seasons = show.seasons
    episodes = show.seasons[1]
    print((seasons, episodes))
    media = rs.scrape(show, 1, 1)
    print(media.url)

def movie():
    rs = DopeBox(Config())
    results = rs.search("Hitman Agent 47")
    print(results)
    movie = results[0]
    media = rs.scrape(movie)
    print(media.url)

if __name__ == "__main__":
    print("To Test if Movies do work: m, for shows: s")
    a = input("Input: ")
    if a.lower() == "m":
        movie()
    else:
        show()
