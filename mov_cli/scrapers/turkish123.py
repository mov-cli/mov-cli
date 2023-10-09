from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from typing import List, Dict, Tuple
   from ..config import Config
   from httpx import Response
   from bs4 import BeautifulSoup, Tag
   from ..http_client import HTTPClient

import re
from .. import utils
from ..scraper import Scraper
from ..media import Series, Metadata, MetadataType
from urllib import parse as p

__all__ = ("Turkish123",)

class Turkish123(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://turkish123.ac"
        super().__init__(config, http_client)

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        page = self.http_client.get(self.base_url + "/" + metadata.id, redirect = True)
        page_soup = self.soup(page)
        year = page_soup.find("div", {"class": "mvici-right"})
        year = year.findAll("a")

        seasons = {}

        seasons[1] = len(page_soup.findAll("a", {"class": "episodi"}))
        return seasons

    def __get_episode_url(self, id: str, episode: int):
        req = self.http_client.get(self.base_url + "/" + id, redirect = True)
        soup = self.soup(req)
        episode = soup.findAll("a", {"class": "episodi"})[episode -1]["href"]
        return episode
            
    def __tukipasti(self, href: str):
        html = self.http_client.get(href).text
        regex = r'''"https:\/\/tukipasti\.com(.*?)"'''
        s = re.findall(regex, html)[0]
        req = self.http_client.get(f"https://tukipasti.com{s}").text
        url = re.findall("var urlPlay = '(.*?)'", req)[0]
        return url, f"https://tukipasti.com{s}"
                
    def scrape(self, metadata: Metadata, limit: int = 10, episode: utils.EpisodeSelector = None) -> Series:
        id, name = self.__search(metadata, limit)[0]

        self.logger.info(f"Found '{name}', scrapping for stream...")

        if episode is None:
            episode = utils.EpisodeSelector()

        href = self.__get_episode_url(id, episode.episode)
        url, referrer = self.__tukipasti(href)

        return Series(
            url = url,
            title = metadata.title,
            referrer = referrer,
            episode = episode.episode,
            season = episode.season,
            subtitles = None
        )
    
    def __search(self, metadata: Metadata, limit: int = None) -> List[Tuple[str, str]]:
        """Searches for show/movie and returns ID."""

        tv_mov = "tv" if metadata.type == MetadataType.SERIES else "movie"

        req = self.http_client.get(f"https://www.themoviedb.org/{tv_mov}/{metadata.id}", redirect = True)

        id = " ".join(str(req.url).split("-")[1:])

        response = self.http_client.get(
            f"{self.base_url}/?s={p.quote(id)}"
        )
        soup = self.soup(response)

        id_list = []
        items: List[Tag] = soup.findAll("div", {"class": "ml-item"})[:limit]

        for item in items:
            title = item.find("a")["oldtitle"]
            id = item.find("a")["href"].split("/")[:-1][-1]

            id_list.append((id, title))

        return id_list

