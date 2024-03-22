"""
Search api used for searching movies and tv series.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Any, Generator, Dict, Literal
    from ...http_client import HTTPClient

from ...media import Metadata, MetadataType, ExtraMetadata, AiringType
from base64 import b64decode
from thefuzz import fuzz

__all__ = ("TheMovieDB",)

class TMDbSerial:
    def __init__(self, data, type: MetadataType):
        self.id: int = data.get("id")
        self.title: str = self.__extract_title(data)
        self.release_date: str = data.get("release_date") or data.get("first_air_date")
        self.year: str = self.release_date[:4] if self.release_date else None
        self.type: MetadataType = type
    
    def __extract_title(self, data):
        title_fields = ["title", "name", "original_title", "original_name"]
        for field in title_fields:
            if field in data:
                return data[field]
        return ""  # If none of the fields are found, return an empty string

class TheMovieDB:
    """API-Wrapper for themoviedb.org"""
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.api_key = str(b64decode("ZDM5MjQ1ZTExMTk0N2ViOTJiOTQ3ZTNhOGFhY2M4OWY="), "utf-8")

        self.metadata = "https://api.themoviedb.org/3/{}/{}?language=en-US&append_to_response=episode_groups,alternative_titles,credits&api_key={}"

        self.search_url = "https://api.themoviedb.org/3/search/{}?query={}&include_adult=false&language=en-US&page=1&api_key={}"


    def search(self, query: str, limit: int = 10) -> Generator[Metadata, Any, None]:
        serial_list: List[TMDbSerial] = []

        movie = self.http_client.get(self.search_url.format("movie", query, self.api_key)).json()["results"]
        tv = self.http_client.get(self.search_url.format("tv", query, self.api_key)).json()["results"]

        for item in movie:
            item = TMDbSerial(item, MetadataType.MOVIE)

            if not item.release_date:
                continue

            serial_list.append(item)

        for item in tv:
            item = TMDbSerial(item, MetadataType.SERIES)

            if not item.release_date:
                continue

            serial_list.append(item)

        sorted_list: List[TMDbSerial] = self.__sort(serial_list, query)[:limit]
        # Is there are point in fuzzy sorting? The search api (tmdb) should do that for us and fzf exists for that reason. ~ Goldy

        # Also yield won't actually do anything performance wise if we've already appended the items into a list.
        # Actually in this case we can't really take advantage of yield as the api returns all results at once. ~ Goldy
        for item in sorted_list:
            yield Metadata(
                id = item.id,
                title = item.title,
                type = item.type,
                year = item.year,
                extra_func = lambda: self.__extra_metadata(item)
            )

    def scrape_episodes(self, metadata: Metadata, **kwargs) -> Dict[int, int] | Dict[None, Literal[1]]:
        scraped_seasons = {}

        seasons = self.http_client.get(self.metadata.format("tv", metadata.id, self.api_key)).json()["seasons"]

        for season in seasons:
            if season["season_number"] == 0:
                continue

            scraped_seasons[season["season_number"]] = season["episode_count"]

        return scraped_seasons

    def __extra_metadata(self, serial: TMDbSerial) -> ExtraMetadata: # This API is dawgshit
        type = "movie" if serial.type == MetadataType.MOVIE else "tv"
        metadata = self.http_client.get(self.metadata.format(type, serial.id, self.api_key)).json()

        description = None
        image_url = None
        cast = None
        alternate_titles = None
        genres = None
        airing = None

        if metadata.get("overview"):
            description = metadata.get("overview")

        if metadata.get("poster_path"):
            image_url = metadata.get("poster_path")

        if metadata["credits"]["cast"]:
            cast = [i.get("name") or i.get("original_name") for i in metadata["credits"]["cast"]]
        
        alternative = metadata["alternative_titles"]

        titles = alternative.get("results") or alternative.get("titles")

        if titles:
            alternate_titles = [(i.get("iso_3166_1"), i.get("title")) for i in titles]

        if metadata["genres"]:
            genres = [i["name"] for i in metadata["genres"]]

        airing_status = metadata["status"]

        if "Released" in airing_status:
            airing = AiringType.RELEASED
        elif "Production" in airing_status:
            airing = AiringType.PRODUCTION
        elif "Returning" in airing_status:
            airing = AiringType.ONGOING
        elif "Canceled" in airing_status:
            airing = AiringType.CANCELED
        else:
            airing = AiringType.DONE

        return ExtraMetadata(
            description = description,
            image_url = image_url,
            cast = cast,
            alternate_titles = alternate_titles,
            genres = genres,
            airing = airing
        )

    def __sort_key(self, query):
        def similarity_score(item: TMDbSerial):
            return fuzz.ratio(item.title, query)
        return similarity_score

    def __sort(self, unsorted, query):
        sorted_list = sorted(unsorted, key=self.__sort_key(query), reverse=True)
        return sorted_list