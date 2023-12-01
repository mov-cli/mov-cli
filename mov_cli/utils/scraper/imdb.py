from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import Tag
    from typing import List
    from ...config import Config

from bs4 import BeautifulSoup
from ...http_client import HTTPClient
from ...media import Metadata, MetadataType

__all__ = ("imdb_search",)

# NOTE: Will probably remove this as I don't think any other scraper will use it and it's not very stable :/
def imdb_search(query: str, config: Config, limit: int = 10) -> List[Metadata]:
    http_client = HTTPClient(config)

    imdb_data = http_client.get(
        f"https://v2.sg.media-imdb.com/suggestion/{query[0]}/{query}.json"
    )
    search_results: List[dict] = imdb_data.json()["d"]

    meta_data_list = []

    for search_result in search_results[:limit]:
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

        soup = BeautifulSoup(
            http_client.get(f"https://www.imdb.com/title/{id}/").text, config.parser
        )

        description = soup.find("span", {"data-testid": "plot-xl"}).text

        storyline_genres = soup.find("li", {"data-testid": "storyline-genres"})
        li_genres: List[Tag] = storyline_genres.find_all("li", {"class": "ipc-inline-list__item"})
        genres = [genre.find("a").text for genre in li_genres]

        meta_data_list.append(
            Metadata(
                id = id,
                title = search_result.get("l"),
                url = None,
                type = imdb_type,
                image_url = image_url,
                year = year,
                genre = genres,
                cast = cast,
                description = description
            )
        )

    return meta_data_list