"""
Search api used for searching movies and tv series.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from typing import List, Generator, Any

from bs4 import BeautifulSoup, Tag

from ..media import Metadata, MetadataType, ExtraMetadata, AiringType

__all__ = ("TheMovieDB",)

# NOTE: Search API's are getting removed!

class TheMovieDB():
    """Wrapper for themoviedb.org"""
    def __init__(self, http_client: HTTPClient) -> None:
        self.http_client = http_client

        self.root_url = "https://www.themoviedb.org"
        self.not_translated = "We don't have an overview translated in English. Help us expand our database by adding one."

    def search(self, query: str) -> Generator[Metadata, Any, None]:
        """Search for shows and films. Returns a generator btw."""
        response = self.http_client.get(self.root_url + "/search", params = {"query": query})
        soup = BeautifulSoup(response.text, self.http_client.config.parser)

        return self.__strip_media_items(soup)

    def __strip_media_items(self, soup: BeautifulSoup) -> Generator[Metadata, Any, None]:
        """Generator that strips 🙄 the media items."""
        movie_items = soup.find("div", {"class": "movie"}).find_all("div", {"class": "card v4 tight"})
        tv_items = soup.find("div", {"class": "tv"}).find_all("div", {"class": "card v4 tight"})

        items: List[Tag] = movie_items + tv_items

        for item in items:
            description = item.find("div", {"class": "overview"}).find("p")
            if description == self.not_translated:
                description = None
                
            release_date = item.find("span", {"class": "release_date"})
            image = item.find("img", {"class": "poster"})
            id = item.find("a")["href"].split("/")[-1]

            yield Metadata(
                id = id,
                title = item.find("h2").text,
                description = description.text if description is not None else "",
                type = MetadataType.MOVIE if "movie" in item.parent.parent.attrs["class"] else MetadataType.SERIES,
                year = release_date.text.split(" ")[-1] if release_date is not None else None,
                image_url = self.root_url + image.attrs["src"].replace("w94_and_h141_bestv2", "w600_and_h900_bestv2") if image is not None else None,
                extra_func = lambda: self.__scrape_extra_metadata(item)
            )

        return None

    def __scrape_extra_metadata(self, item: Tag) -> ExtraMetadata:
        url = self.root_url + item.find("a")["href"]

        soup = BeautifulSoup(self.http_client.get(url, redirect = True).text, self.http_client.config.parser)

        soup_c = BeautifulSoup(self.http_client.get(url + "/cast", redirect = True).text, self.http_client.config.parser)

        cast = []
        alternate_titles = []
        genres = []
        airing = None

        airing_status = soup.find("section", {"class": "facts left_column"}).find("p").contents[-1].text

        if airing_status.__contains__("Released"):
            airing = AiringType.RELEASED
        elif airing_status.__contains__("Production"):
            airing = AiringType.PRODUCTION
        elif airing_status.__contains__("Returning"):
            airing = AiringType.ONGOING
        else:
            airing = AiringType.DONE

        genre: List[Tag] = soup.find("span", {"class":"genres"}).findAll("a")

        people: List[Tag] = []
        people_credits = soup_c.find("ol", {"class":"people credits"})

        if people_credits is not None: # This doesn't always exists apparently.
            people = people_credits.findAll("li")

        for g in genre:
            genres.append(g.text)

        if soup.find_all("p", {"class": "wrap"}):
            alternate_titles.append(soup.find("p", {"class": "wrap"}).contents[-1].text)
        
        for i in people:
            cast.append(i.select("p:nth-child(1) > a:nth-child(1)")[0].text)

        return ExtraMetadata(
            alternate_titles = alternate_titles,
            cast = cast,
            genre = genres,
            airing = airing
        )



