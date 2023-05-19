import re

import httpx
from bs4 import BeautifulSoup as BS

def get_imdb_id(query: str) -> str:
    query = query.replace(" ", "_")
    req = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json"
    ).json()["d"]
    print(req)
    return req[0]["id"]


def get_imdb_title(query: str) -> str:
    query = query.replace(" ", "-")
    req = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json"
    ).json()["d"][0]["l"]
    return req


def get_imdb_title_and_img(query: str) -> str:
    query = query.replace(" ", "-")
    req = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json"
    ).json()
    title = req["d"][0]["l"]
    img = req["d"][0]["i"]["imageUrl"]
    return title, img


def get_season_seasons(tmdb_id: str, name: str) -> int:
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/seasons"
    ).text
    rem = BS(req, self.parser)
    seasons = [i.text for i in rem.select(".flex > div.season_wrapper")]
    return len(seasons)


def get_season_episodes(tmdb_id: str, name: str, season_number: str) -> int:
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/season/{season_number}"
    ).text
    episodes = int(BS(req, self.parser).select_one(".episode_sort.space > span").text)
    return episodes


def parse(text: str) -> str:
    return re.sub(r"\W+", "-", text.lower())
