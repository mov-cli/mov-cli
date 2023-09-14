from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from typing import List
   from httpx import Response
   from ..config import Config
   from bs4 import BeautifulSoup

from ..media import Metadata, MetadataType, Series
import re
from .. import scraper_utils
from ..scraper import Scraper

class ViewAsian(Scraper):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://viewasian.co"
        super().__init__(config)

    def search(self, query: str) -> List[Metadata]:
        query = query.replace(' ', '-')
        result = self.__results(query)
        return result

    def __results(self, query: str) -> List[Metadata]:
        metadata_list = []

        page = 0

        while True:
            page += 1
            response = self.get(f"{self.base_url}/movie/search/{query}?page={page}")

            soup = self.soup(response)

            items = soup.findAll("a", {"class": "ml-mask"})

            if len(items) == 0:
                break

            for item in items:
                item : BeautifulSoup

                data_url = item["data-url"]
                title = item["title"]
                id = item["href"].split("/")[-1]
                img = item.select(".mli-thumb")[0]["data-original"]

                data_url_req = self.get(self.base_url + data_url)
                data_soup = self.soup(data_url_req)

                year = data_soup.find("div", {"class": "jt-imdb"})

                episodes = item.find("span", {"class": "mli-eps raw"}).find("i").text

                metadata_list.append(Metadata(
                    title = title,
                    id = id,
                    type = MetadataType.SERIES,
                    image_url = img,
                    seasons = {1: episodes},
                    year = year  
                ))

        return metadata_list

    def dood(self, url):
        video_id = url.split("/")[-1]
        webpage_html = self.get(
            f"https://dood.to/e/{video_id}", redirect = True
        )
        webpage_html = webpage_html.text
        try:
            pass_md5 = re.search(r"/pass_md5/[^']*", webpage_html).group()
        except:
            return None
        urlh = f"https://dood.to{pass_md5}"
        headers = {
            "referer": "https://dood.to",
        }
        self.add_header_elem(headers)
        res = self.get(urlh).text
        md5 = pass_md5.split("/")
        true_url = res + "MovCli3oPi?token=" + md5[-1]
        return true_url
    
    def streamwish(self, url):
        req = self.get(url).text
        file = re.findall(r'file:"(.*?)"', req)[0]
        return file
    
    def cdn(self, id: str, episode: int) -> str:
        req = self.get(self.base_url + f"/watch/{id}/watching.html?ep={episode}")
        soup = self.soup(req)
        
        base_url = soup.find("li", {"class": "doodstream"})["data-video"]
        url = self.dood(base_url)
        if not url:
            self.logger.debug("Doodstream returned no URL")
            base_url = soup.find("li", {"class": "streamwish"})["data-video"]
            url = self.streamwish(base_url)

        return url, base_url

    def scrape(self, metadata: Metadata, episode: int = None) -> Series:
        url, referrer = self.cdn(metadata.id, episode)

        return Series(
            url = url,
            title = metadata.title,
            referrer = referrer,
            episode = episode,
            season = 1,
            subtitles = None
        )