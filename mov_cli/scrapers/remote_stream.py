from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config
    from ..http_client import HTTPClient
    from typing import List, Dict, Tuple

import re

from ..scraper import Scraper
from urllib.parse import quote
from ..media import Series, Movie, MetadataType, Metadata

__all__ = ("RemoteStream",)

class RemoteStream(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://remotestre.am"
        self.catalogue = self.base_url + "/catalogue?display=plain"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"
        self.imdb_media = "https://v2.sg.media-imdb.com"

        super().__init__(config, http_client)

    def scrape(self, metadata: Metadata, limit: int = 10, season: int = None, episode: int = None) -> Series | Movie:
        id, imdb_search_result  = self.__search(metadata, limit = limit)[0]

        self.logger.info(f"Found '{imdb_search_result.get('l')}', scrapping for stream...")

        if metadata.type == MetadataType.SERIES:
            url = self.__cdn(id, season, episode)

            return Series(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                episode = episode,
                season = season,
                subtitles = None
            )
        else:       
            url = self.__cdn(id)

            return Movie(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                year = metadata.year,
                subtitles = None
            )

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

    def __search(self, metadata: Metadata, limit: int = 10) -> List[Tuple[str, dict]]:
        query = f"{metadata.title} {metadata.year}"

        imdb_data = self.http_client.get(
            self.imdb_media + f"/suggestion/{quote(query[0])}/{quote(query)}.json"
        )
        imdb_search_results: List[dict] = imdb_data.json()["d"]

        catalogue = self.http_client.get(self.catalogue)

        id_list = []

        for search_result in imdb_search_results[:limit]:
            id = search_result.get("id")

            if id is None or not id.startswith("tt") or id not in catalogue.text:
                continue

            id_list.append((id, search_result))

        return id_list

    def __cdn(self, imdb_id: str, season: int = None, episode: int = None) -> str:
        url = self.base_url + f"/e/?imdb={imdb_id}"

        if season and episode:
            url += f"&s={season}&e={episode}"

        req = self.http_client.get(url).text
        return re.findall('"file":"(.*?)"', req)[0]