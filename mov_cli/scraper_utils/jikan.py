from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from ..media import Metadata
    from ..http_client import HTTPClient

from ..media import Metadata, MetadataType

class Jikan(): # NOTE: Might remove and scrap this in the future.
    """Api wrapper for the Jikan v4 anime api."""
    def __init__(self, http_client: HTTPClient) -> None:
        self.http_client = http_client

    def search_anime(self, query: str, limit: int = 25) -> List[Metadata]:
        """Search for an anime via jikan api."""
        response = self.http_client.get(
            f"https://api.jikan.moe/v4/anime", params = {"q": query, "limit": limit}
        )

        json_response = response.json()

        return [
            Metadata(
                title = anime["title"],
                id = str(anime["mal_id"]),
                type = MetadataType.MOVIE if anime["type"] == "Movie" else MetadataType.SERIES,
                year = str(anime["year"]) if anime["year"] is not None else None,
                image_url = anime["images"]["jpg"].get("large_image_url")
            ) for anime in json_response["data"]
        ]