from mov_cli.config import Config
from mov_cli.scrapers import RemoteStream

from devgoldyutils import pprint

if __name__ == "__main__":
    rs = RemoteStream(Config())
    shows = rs.search("The Grand Tour")
    pprint(shows)
    show = shows[0]
    seasons = show.seasons
    episodes = show.seasons[1]
    pprint((seasons, episodes))
    media = rs.scrape(show, 1, 1)
    pprint(media.url)