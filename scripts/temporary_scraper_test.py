from mov_cli.scrapers import RemoteStream

if __name__ == "__main__":
    rs = RemoteStream()
    a = rs.search("The Grand Tour")
    print(a)
    rs.select(1)
    seasons = rs.get_seasons()
    episodes = rs.get_episodes(1)
    print(seasons, episodes)
    a = rs.get_media(1, 1)
    print(a.url)