import re

import httpx
from bs4 import BeautifulSoup as BS


def get_tmdb_id(query: str) -> list:
    req, res = (
        httpx.get(f"https://www.themoviedb.org/search?query={query}").text,
        httpx.get(f"https://www.themoviedb.org/search/tv?query={query}").text,
    )
    rem, ram = BS(req, "lxml"), BS(res, "lxml")
    titles = [i.text for i in rem.select("a.result > h2")] + [
        i.text for i in ram.select("a.result > h2")
    ]
    url = [f"https://olgply.com{i['href']}" for i in rem.select("a.result")] + [
        f"https://https://olgply.com{i['href']}" for i in ram.select("a.result")
    ]
    tmdb_id = [re.sub(r"\D+", "", i) for i in url]
    mv_tv = ["MOVIE" if i.__contains__("movie") else "TV" for i in url]
    return [list(i) for i in zip(titles, url, tmdb_id, mv_tv)]
    # TODO title, url , id, mv_tv


def get_imdb_id(query: str) -> str:
    query = query.replace(" ", "_")
    req = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json"
    ).json()["d"]
    print(req)
    return req[0]["id"]

def get_imdb_title(query: str) -> str:
    query = query.replace(" ", "-")
    req = httpx.get(f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json").json()["d"][0]["l"]
    return req

def get_imdb_title_and_img(query: str) -> str:
    query = query.replace(" ", "-")
    req = httpx.get(f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json").json()
    title = req["d"][0]["l"]
    img = req["d"][0]["i"]["imageUrl"]
    return title, img

def get_season_seasons(tmdb_id: str, name: str) -> int:
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/seasons"
    ).text
    rem = BS(req, "lxml")
    seasons = [i.text for i in rem.select(".flex > div.season_wrapper")]
    return len(seasons)


def get_season_episodes(tmdb_id: str, name: str, season_number: str) -> int:
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/season/{season_number}"
    ).text
    episodes = int(BS(req, "lxml").select_one(".episode_sort.space > span").text)
    return episodes


def parse(text: str) -> str:
    return re.sub(r"\W+", "-", text.lower())
