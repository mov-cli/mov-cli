"""
Search api used for searching dramas.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Generator, Any
    from ..http_client import HTTPClient

from ..media import Metadata, MetadataType, ExtraMetadata, AiringType
from bs4 import BeautifulSoup

__all__ = ("Dizilah",)

class Dizilah():
    """Api wrapper for dizilah"""
    def __init__(self, http_client: HTTPClient) -> None:
        self.http_client = http_client

    def search(self, query: str, limit: int = 25) -> Generator[Metadata, Any, None]:
        """Search for an drama via dizilah."""
        response = self.http_client.get(
            f"https://dizilah.com/api/search/tv?include=genres&keyword={query}&limit={limit}"
        )

        json_response = response.json()

        for drama in json_response:
            yield Metadata(
                    title = drama["title"],
                    id = drama["hashid"],
                    description = drama["synopsis"],
                    type = MetadataType.SERIES,
                    year = drama["year"],
                    image_url = drama["poster"],
                    extra_func = lambda: self.__scrape_extra_metadata(drama)
                )
            
        return None

    def __scrape_extra_metadata(self, item) -> ExtraMetadata:
        genres = []
        cast = []
        airing = AiringType.DONE

        for genre in item["genres"]:
            genres.append(genre["name"])
        
        if item["status"] == "Running":
            airing = AiringType.ONGOING

        req = self.http_client.get(item["url"] + "/cast")

        soup = BeautifulSoup(req.text, self.http_client.config.parser)

        for name in soup.findAll("p", {"itemprop": "name"}):
            cast.append(name.find("a").text)
        
        return ExtraMetadata(
            alternate_titles = None,
            cast = cast,
            genre = genres,
            airing = airing
        )

