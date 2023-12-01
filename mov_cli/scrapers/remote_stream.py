from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config
    from ..http_client import HTTPClient
    from typing import List, Dict

import re
from .. import utils

from ..scraper import Scraper
from ..media import Series, Movie, MetadataType, Metadata
from ..utils.scraper import TheMovieDB

__all__ = ("RemoteStream",)

class RemoteStream(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://remotestre.am"
        self.mov_catalogue = self.base_url + "/listing?type=movie"
        self.tv_catalogue = self.base_url + "/listing?type=serie"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"
        self.imdb_media = "https://v2.sg.media-imdb.com"
        self.api_key = "fb7bb23f03b6994dafc674c074d01761"
        self.search_api = TheMovieDB(http_client)

        super().__init__(config, http_client)

    def scrape(self, metadata: Metadata, episode: utils.EpisodeSelector = None) -> Series | Movie:

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
            episodes_url = f"https://www.themoviedb.org/tv/{metadata.id}/seasons"
            html = self.http_client.get(episodes_url, redirect=True).text
            seasons_soup = self.soup(html)

            for season in range(len(seasons_soup.findAll("div", {"class": "season_wrapper"}))):
                seasons_response = self.http_client.get(f"https://www.themoviedb.org/tv/{metadata.id}/season={season + 1}")
                
                chicken_noodle_soup = self.soup(seasons_response)

                if chicken_noodle_soup.find("div", {"class": "error_wrapper"}):
                    break

                seasons[season + 1] = len(chicken_noodle_soup.findAll("div", {"class": "card"}))

            return seasons

        return {None: 1}

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        catalogue = self.http_client.get(self.mov_catalogue).text + self.http_client.get(self.tv_catalogue).text
        catalogue = catalogue.split("<br>")

        returnable_results = []

        search_results = self.search_api.search(query)[:limit]

        for search_result in search_results:
            if search_result.id in catalogue:
                returnable_results.append(search_result)

        return returnable_results


    def __cdn(self, imdb_id: str, episode: utils.EpisodeSelector = None) -> str:
        url = self.base_url + f"/e/?tmdb={imdb_id}"

        if episode is not None and episode.season and episode:
            url += f"&s={episode.season}&e={episode.episode}"

        req = self.http_client.get(url).text
        return re.findall('"file":"(.*?)"', req)[0]