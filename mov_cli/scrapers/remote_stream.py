from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Dict
    from ..config import Config
    from ..http_client import HTTPClient

import re

from .. import scraper_utils
from ..scraper import Scraper
from ..media import Series, Movie, MetadataType, Metadata

__all__ = ("RemoteStream",)

class RemoteStream(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://remotestre.am"
        self.catalogue = "https://remotestre.am/catalogue?display=plain"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"

        super().__init__(config, http_client)

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        imdb_metadata_list = scraper_utils.imdb_search(query, self.config, limit)
        catalogue = self.http_client.get(self.catalogue)

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

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        if metadata.type == MetadataType.SERIES:
            seasons = {}
            episodes_url = f"https://www.imdb.com/title/{metadata.id}/episodes/"
            html = self.http_client.get(episodes_url).text
            seasons_soup = self.soup(html)

            for season in range(1, len(seasons_soup.findAll("li", {"data-testid": "tab-season-entry"}))):
                seasons_response = self.http_client.get(episodes_url + f"?season={season}")
                chicken_noodle_soup = self.soup(seasons_response)

                seasons[season] = len(chicken_noodle_soup.findAll("article", {"class": "episode-item-wrapper"}))

            return seasons

        return {None: 1}

    def scrape(self, metadata: Metadata, season: int = None, episode: int = None,) -> Series | Movie:
        if metadata.type == MetadataType.SERIES:
            url = self.__cdn(metadata, season, episode)

            return Series(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                episode = episode,
                season = season,
                subtitles = None
            )
        else:       
            url = self.__cdn(metadata)

            return Movie(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                year = metadata.year,
                subtitles = None
            )

    def __cdn(self, metadata: Metadata, season: int = None, episode: int = None) -> str:
        url = f"https://remotestre.am/e/?imdb={metadata.id}"

        if season and episode:
            url += f"&s={season}&e={episode}"

        req = self.http_client.get(url).text
        return re.findall('"file":"(.*?)"', req)[0]