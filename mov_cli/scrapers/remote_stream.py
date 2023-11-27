from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..config import Config
    from ..http_client import HTTPClient
    from typing import List, Dict, Tuple

import re
from .. import utils
from urllib.parse import quote

from ..scraper import Scraper
from ..media import Series, Movie, MetadataType, Metadata

__all__ = ("RemoteStream",)

# Hinting for the IMDB result dictionary because no type hint drives me nuts!!! 😡💢
IData = TypedDict("IData", {"height": int, "imageUrl": str, "width": int})

class IMDBSearchResultData(TypedDict):
    i: IData
    id: str
    l: str
    q: str
    qid: str
    rank: int
    s: str
    y: int


class RemoteStream(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://remotestre.am"
        self.catalogue = self.base_url + "/catalogue?display=plain"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"
        self.imdb_media = "https://v2.sg.media-imdb.com"

        super().__init__(config, http_client)

    def scrape(self, metadata: Metadata, episode: utils.EpisodeSelector = None) -> Series | Movie:
        self.logger.info(f"Got '{metadata.title}', scrapping for stream...")

        if metadata.type == MetadataType.SERIES:
            if episode is None:
                episode = utils.EpisodeSelector()

            url = self.__cdn(metadata.id, episode)

            return Series(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                episode = episode.episode,
                season = episode.season,
                subtitles = None
            )
        else:    
            url = self.__cdn(metadata.id)

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

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        imdb_data = self.http_client.get(
            self.imdb_media + f"/suggestion/{quote(query[0])}/{quote(query)}.json"
        )
        imdb_search_results: List[IMDBSearchResultData] = imdb_data.json()["d"]

        # TODO: This is returning internal server error. We need a fix.
        catalogue = self.http_client.get(self.catalogue)

        results = []

        for search_result in imdb_search_results[:limit]:
            id = search_result.get("id")

            if id is None or not id.startswith("tt") or id not in catalogue.text:
                continue

            results.append(
                Metadata(
                    id, 
                    title = search_result["l"],
                    type = MetadataType.MOVIE if search_result["qid"].lower() in ["movie", "tvmovie"] else MetadataType.SERIES
                )
            )

        return results

    def __cdn(self, imdb_id: str, episode: utils.EpisodeSelector = None) -> str:
        url = self.base_url + f"/e/?imdb={imdb_id}"

        if episode is not None and episode.season and episode:
            url += f"&s={episode.season}&e={episode}"

        req = self.http_client.get(url).text
        return re.findall('"file":"(.*?)"', req)[0]