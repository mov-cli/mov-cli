from __future__ import annotations
from typing import TYPE_CHECKING

from ..media import Metadata, LiveTV, MetadataType

if TYPE_CHECKING:
    from typing import List
    from httpx import Response
    from ..config import Config
    from bs4 import BeautifulSoup
    from ..http_client import HTTPClient

from ..scraper import Scraper
from re import findall
from dataclasses import dataclass
from urllib.parse import unquote

@dataclass
class MetadataEja:
    id: str
    url: str | None
    title: str | None
    type: str | None
    country: str | None

__all__ = ("Eja",)

class Eja(Scraper): # TODO: Add scrape_metadata_episodes abstract method.
    def __init__(self, config: Config, http_client: HTTPClient):
        super().__init__(config, http_client)

        self.base_url = "https://eja.tv"

    def search(self, q: str = None, limit: int = None):
        q = q.replace(" ", "+")
        eja_req = self.http_client.get(f"{self.base_url}/?search={q}")
        result = self.__results(eja_req, limit)
        return result

    def __results(self, response: Response, limit: int = None) -> List[MetadataEja]:
        soup = self.soup(response)
        col = soup.findAll("div", {"class": "col-sm-4"})[:limit]

        metadata_eja = []

        for item in col:
            item: BeautifulSoup

            a = item.findAll("a")
            country = a[0].find("img")["alt"]
            title = a[1].text
            url = a[1]["href"]
            id = url[1:]
        
            metadata_eja.append(MetadataEja(
                id = id,
                url = self.base_url + url,
                title = title, 
                type = MetadataType.LIVE_TV,
                country = country
                ))
        
        return metadata_eja

    
    def scrape(self, metadata: Metadata, season: int = None, episode: int = None) -> LiveTV:
        url = self.__get_hls(metadata.id)
        return LiveTV(url, metadata.title, self.base_url)

    def __get_hls(self, url):
        link = self.http_client.get(f"https://eja.tv/?{url}", redirect=True)
        link = str(link.url)    
        return unquote(findall("\?(.*)#", link)[0])