"""
Search api used for searching anime.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Generator, Any
    from ..http_client import HTTPClient

from ..media import Metadata, MetadataType, AiringType, ExtraMetadata

class Jikan(): # NOTE: Might remove and scrap this in the future.
    """Api wrapper for the Jikan v4 anime api."""
    def __init__(self, http_client: HTTPClient) -> None:
        self.http_client = http_client

    def search(self, query: str, limit: int = 25) -> Generator[Metadata, Any, None]:
        """Search for an anime via jikan api."""
        response = self.http_client.get(
            "https://api.jikan.moe/v4/anime", params = {"q": query, "limit": limit}
        )

        json_response = response.json()

        for anime in json_response["data"]:

            yield Metadata(
                    title = anime["title"],
                    id = str(anime["mal_id"]),
                    description = anime["synopsis"],
                    type = MetadataType.MOVIE if anime["type"] == "Movie" else MetadataType.SERIES,
                    year = str(anime["year"]) if anime["year"] is not None else None,
                    image_url = anime["images"]["jpg"].get("large_image_url"),
                    extra_func = lambda: self.__scrape_extra_metadata(anime)
                )
        return None
    
    def __scrape_extra_metadata(self, item) -> ExtraMetadata:
        alternate_titles = []
        genres = []
        airing = AiringType.DONE

        for genre in item["genres"]:
            genres.append(genre["name"])
        
        if item["status"] == "Currently Airing":
            airing = AiringType.ONGOING

        alternate_titles.append(item["title_japanese"])

        for title in item["title_synonyms"]:
            alternate_titles.append(title)
        
        return ExtraMetadata(
            alternate_titles = alternate_titles,
            cast = None,
            genre = genres,
            airing = airing
        )