from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from typing import List, Dict
   from ..config import Config
   from httpx import Response
   from bs4 import BeautifulSoup
   from ..http_client import HTTPClient

import re

from ..scraper import Scraper
from ..media import Series, Metadata, MetadataType

class Turkish123(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://turkish123.ac"
        super().__init__(config, http_client)

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        query = query.replace(' ', '+')
        req = self.http_client.get(f'{self.base_url}/?s={query}')
        result = self.__results(req, limit)
        return result

    def __results(self, response: Response, limit: int = None) -> List[Metadata]:
        metadata_list = []
        soup = self.soup(response)
        mlitem = soup.findAll("div", {"class": "ml-item"})[:limit]

        for item in mlitem:
            item: BeautifulSoup
            if item.select(".mli-quality")[0].text == "COMING SOON":
                continue
            title = item.find("a")["oldtitle"]
            id = item.find("a")["href"].split("/")[:-1][-1]

            url = item.find("a")["href"]

            img = item.select(".mli-thumb")[0]["src"]
            
            year = None

            page = self.http_client.get(self.base_url + "/" + id, redirect = True)
            page_soup = self.soup(page)
            
            year = page_soup.find("div", {"class": "mvici-right"})
            year = year.findAll("a")

            if len(year) == 2:
                year = year[0].text + "-" + year[1].text
            else:
                year = year[0].text
            
            mvici = page_soup.find("div", {"class": "mvici-left"}).findAll("p")

            genre = [i.text for i in mvici[2].findAll("a")]

            cast = [i.text for i in mvici[3].findAll("a")]

            description = page_soup.find("p", {"class": "f-desc"}).text

            metadata_list.append(Metadata(
                title = title,
                id = id,
                url = url,
                type = MetadataType.SERIES,
                image_url = img,
                year = year,
                genre = genre,
                cast = cast,
                description = description
            ))
        
        return metadata_list

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
                
    def scrape(self, metadata: Metadata, episode: int = None, season: int = None) -> Series:
        if episode is None:
            episode = 1
        if season is None:
            season = 1

        href = self.__get_episode_url(metadata.id, episode)
        url, referrer = self.__tukipasti(href)

        return Series(
            url = url,
            title = metadata.title,
            referrer = referrer,
            episode = episode,
            season = season,
            subtitles = None
        )
        
