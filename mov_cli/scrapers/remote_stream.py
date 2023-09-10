from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from ..config import Config
    from .scraper_utils.imdb import IMDBMetadata

import re

from . import Scraper, scraper_utils
from ..media import Series, Movie, MetadataType

class RemoteStream(Scraper):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://remotestre.am"
        self.catalogue = "https://remotestre.am/catalogue?display=plain"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"

        super().__init__(config)

    def search(self, query: str) -> List[IMDBMetadata]:
        imdb_metadata_list = scraper_utils.imdb_search(query, self.config)
        catalogue = self.get(self.catalogue)

        metadata_list = []

        for metadata in imdb_metadata_list:
            id = metadata.id

            if id is not None:
                if not id.startswith("tt"):
                    continue
                if id not in catalogue.text:
                    continue

                metadata_list.append(
                    metadata
                )

        return metadata_list

    def scrape(self, metadata: IMDBMetadata, episode: int = None, season: int = None) -> Series | Movie:
        if metadata.type == MetadataType.SERIES:
            media = self.__tv(metadata, season, episode)
        else:
            media = self.__movie(metadata)

        return media

    def cdn(self, metadata: IMDBMetadata, season: int = None, episode: int = None) -> str:
        url = f"https://remotestre.am/e/?imdb={metadata.id}"

        if season and episode:
            url += f"&s={season}&e={episode}"

        req = self.get(url).text
        return re.findall('"file":"(.*?)"', req)[0]

    def __tv(self, metadata: IMDBMetadata, season: int, episode: int) -> Series:
        url = self.cdn(metadata, season, episode)

        #__dict = self.make_json(
        #    self.__selected.get("title"),
        #    url,
        #    "show",
        #    self.base_url,
        #    self.__selected.get("img"),
        #    self.get_seasons(),
        #    season,
        #    episode,
        #    self.__selected.get("year")
        #)

        return Series(
            url = url,
            title = metadata.title,
            referrer = self.base_url,
            episode = episode,
            season = season
        )

    def __movie(self, metadata: IMDBMetadata) -> Movie:
        url = self.cdn(metadata)
        #__dict = self.make_json(
        #    self.__selected.get("title"),
        #    url,
        #    "movie",
        #    self.base_url,
        #    self.__selected.get("img"),
        #    year=self.__selected.get("year")
        #)
        return Movie(
            url = url,
            title = metadata.title,
            referrer = self.base_url,
            year = metadata.year
        )