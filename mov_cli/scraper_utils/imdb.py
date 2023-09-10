from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from ..config import Config

import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from ..media import Metadata, MetadataType

__all__ = ("imdb_search", "IMDBMetadata")

@dataclass
class IMDBMetadata(Metadata):
    id: str # NOTE: Everything has a id ~ Ananas

def imdb_search(query: str, config: Config) -> List[IMDBMetadata]:
    imdb_data = httpx.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0]}/{query}.json"
    )
    search_results: List[dict] = imdb_data.json()["d"]

    meta_data_list = []

    for search_result in search_results:
        id = search_result.get("id")

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

        seasons = None

        if imdb_type == MetadataType.SERIES:
            seasons = {}
            episodes_url = f"https://www.imdb.com/title/{id}/episodes/"
            seasons_soup = BeautifulSoup(httpx.get(episodes_url, headers = config.headers).text, config.parser)

            for season in range(1, len(seasons_soup.findAll("li", {"data-testid": "tab-season-entry"}))):
                seasons_response = httpx.get(episodes_url + f"?season={season}", headers = config.headers)
                chicken_noodle_soup = BeautifulSoup(seasons_response.text, config.parser)

                seasons[season] = len(chicken_noodle_soup.findAll("article", {"class": "episode-item-wrapper"}))

        meta_data_list.append(
            IMDBMetadata(
                id = id,
                title = search_result.get("l"),
                type = imdb_type,
                image_url = image_url,
                seasons = seasons,
                year = year
            )
        )

    return meta_data_list