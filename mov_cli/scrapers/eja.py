from __future__ import annotations
from typing import TYPE_CHECKING

from ..media import Metadata, TV, MetadataType

if TYPE_CHECKING:
    from ..config import Config
    from httpx import Response
    from bs4 import BeautifulSoup

from ..scraper import Scraper
from re import findall
from dataclasses import dataclass

@dataclass
class MetadataEja:
    id: str
    title: str
    type: str
    country: str

__all__ = ("eja",)

class eja(Scraper):
    def __init__(self, config: Config):
        super().__init__(config)
        self.base_url = "https://eja.tv"


    def search(self, q: str = None):
        q = q.replace(" ", "+")
        eja_req = self.get(f"{self.base_url}/?search={q}")
        result = self.__results(eja_req)
        return result

    def __results(self, response: Response) -> list:
        soup = self.soup(response)
        col = soup.findAll("div", {"class": "col-sm-4"})

        metadata_eja = []

        for item in col:
            item: BeautifulSoup
            a = item.findAll("a")
            country = a[0].find("img")["alt"]
            title = a[1].text
            id = a[1]["href"][1:]
        
            metadata_eja.append(MetadataEja(
                id = id, 
                title = title, 
                type = MetadataType.TV,
                country = country
                ))
        
        return metadata_eja

    
    def scrape(self, metadata: Metadata, season: int = None, episode: int = None) -> TV:
        url = self.__get_hls(metadata.id)
        return TV(url, metadata.title, self.base_url)

    def __get_hls(self, url):
        link = self.get(f"https://eja.tv/?{url}", redirect=True)
        link = str(link.url)    
        return findall("\?(.*)#", link)[0]