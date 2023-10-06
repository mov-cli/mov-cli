"""
Search api used for searching movies and tv series.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from typing import List, Generator, Any

from bs4 import BeautifulSoup, Tag

from ..media import Metadata, MetadataType

__all__ = ("TheMovieDB",)

class TheMovieDB():
    """Wrapper for themoviedb.org"""
    def __init__(self, http_client: HTTPClient) -> None:
        self.http_client = http_client

        self.root_url = "https://www.themoviedb.org"

    def search(self, query: str) -> Generator[Metadata, Any, None]:
        """Search for shows and films. Returns a generator btw."""
        response = self.http_client.get(self.root_url + "/search", params = {"query": query})
        soup = BeautifulSoup(response.text, self.http_client.config.parser)

        movie_items = soup.find("div", {"class": "movie"}).find_all("div", {"class": "card v4 tight"})
        tv_items = soup.find("div", {"class": "tv"}).find_all("div", {"class": "card v4 tight"})

        return self.__strip_media_items(movie_items + tv_items)

    def __strip_media_items(self, items: List[Tag]) -> Generator[Metadata, Any, None]:
        """Generator that strips 🙄 the media items."""
        for item in items:
            description = item.find("div", {"class": "overview"}).find("p")
            release_date = item.find("span", {"class": "release_date"})
            image = item.find("img", {"class": "poster"})

            yield Metadata(
                id = None, # TODO: Return something other than None.
                title = item.find("h2").text,
                description = description.text if description is not None else "",
                type = MetadataType.MOVIE if "movie" in item.parent.parent.attrs["class"] else MetadataType.SERIES,
                year = release_date.text.split(" ")[-1] if release_date is not None else None,
                image_url = self.root_url + image.attrs["src"].replace("w94_and_h141_bestv2", "w600_and_h900_bestv2") if image is not None else None
            )