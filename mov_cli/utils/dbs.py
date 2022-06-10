import re

import httpx
from bs4 import BeautifulSoup as BS


def get_tmdb_id(query: str):
    req, res = (
        httpx.get(f"https://www.themoviedb.org/search?query={query}").text,
        httpx.get(f"https://www.themoviedb.org/search/tv?query={query}").text,
    )
    rem, ram = BS(req, "html.parser"), BS(res, "html.parser")
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


def get_imdb_id(query):
    query = query.replace(" ", "_")
    req = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0].lower()}/{query}.json"
    ).json()["d"]
    print(req)
    return req[0]["id"]


def get_season_seasons(tmdb_id, name):
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/seasons"
    ).text
    rem = BS(req, "html.parser")
    seasons = [i.text for i in rem.select(".flex > div.season_wrapper")]
    return len(seasons)


def get_season_episodes(tmdb_id, name, season_number):
    req = httpx.get(
        f"https://www.themoviedb.org/tv/{tmdb_id}-{parse(name)}/season/{season_number}"
    ).text
    episodes = int(BS(req, "html.parser").select_one(".episode_sort.space > span").text)
    return episodes


def parse(text: str):
    return re.sub("\W+", "-", text.lower())
