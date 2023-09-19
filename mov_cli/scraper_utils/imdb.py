from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from ..config import Config

import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from ..media import Metadata, MetadataType

__all__ = ("imdb_search",)

def imdb_search(query: str, config: Config) -> List[Metadata]:
    imdb_data = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0]}/{query}.json"
    )
    search_results: List[dict] = imdb_data.json()["d"]

    meta_data_list = []

    for search_result in search_results:
        id = search_result.get("id")

        if not id.startswith("tt"):
            continue

        imdb_type = None # NOTE: I really hope this doesn't cause future chaos. :) I'll change it later.
        qid = search_result.get("qid")

        if qid in ["tvSeries", "tvSpecial"]:
            imdb_type = MetadataType.SERIES
        elif qid in ["movie", "tvMovie"]:
            imdb_type = MetadataType.MOVIE

        image_url = None
        image = search_result.get("i")

        if image is not None:
            image_url = image["imageUrl"]

        year = search_result.get("yr")
        if year is None:
            year = str(search_result.get("y"))

        cast = search_result.get("s").split(", ")

        imdb_page = f"https://www.imdb.com/title/{id}"
        imdb_soup = BeautifulSoup(httpx.get(imdb_page, headers = config.headers).text, config.parser)

        description = imdb_soup.find("span", {"data-testid": "plot-xl"}).text

        genre = imdb_soup.find("li", {"data-testid": "storyline-genres"}).findAll("li")

        genre = [s.find("a").text for s in genre]

        meta_data_list.append(
            Metadata(
                id = id,
                title = search_result.get("l"),
                url = None,
                type = imdb_type,
                image_url = image_url,
                year = year,
                genre = genre,
                cast = cast,
                description = description
            )
        )

    return meta_data_list