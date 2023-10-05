from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from typing import List, Dict
   from ..config import Config
   from bs4 import BeautifulSoup
   from ..http_client import HTTPClient

import re
from ..media import Metadata, MetadataType, Series

from ..scraper import Scraper

class ViewAsian(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://viewasian.co"
        super().__init__(config, http_client)

    def search(self, query: str, limit: int = None) -> List[Metadata]:
        query = query.replace(' ', '-')
        result = self.__results(query, limit)
        return result

    def __results(self, query: str, limit: int = None) -> List[Metadata]:
        metadata_list = []

        page = 0

        while True:
            page += 1
            response = self.http_client.get(f"{self.base_url}/movie/search/{query}?page={page}")

            soup = self.soup(response)

            items = soup.findAll("a", {"class": "ml-mask"})

            if len(items) == 0:
                break

            for item in items:
                item : BeautifulSoup

                data_url = item["data-url"]
                title = item["title"]
                url = item["href"]
                id = url.split("/")[-1]
                img = item.select(".mli-thumb")[0]["data-original"]

                self.http_client.set_header({"X-Requested-With": "XMLHttpRequest"})

                data_url_req = self.http_client.get(self.base_url + data_url)
                data_soup = self.soup(data_url_req)

                description = data_soup.find("p", {"class": "f-desc"}).text

                year = data_soup.find("div", {"class": "jt-imdb"})

                genre = data_soup.findAll("div", {"class": "block"})[1].findAll("a")

                genre = [i.text.strip(", ") for i in genre]

                metadata_list.append(Metadata(
                    title = title,
                    id = id,
                    url = self.base_url + url,
                    type = MetadataType.SERIES,
                    image_url = img,
                    year = year,
                    genre = genre,
                    cast = None,
                    description = description
                ))

                if len(metadata_list) == limit:
                    break

        return metadata_list

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        req = self.http_client.get(metadata.url)
        soup = self.soup(req)
        episodes = soup.findAll("li", {"class": "ep-item"})
        return {None: len(episodes)}

    def dood(self, url):
        video_id = url.split("/")[-1]
        webpage_html = self.http_client.get(
            f"https://dood.to/e/{video_id}", redirect = True
        )
        webpage_html = webpage_html.text
        try:
            pass_md5 = re.search(r"/pass_md5/[^']*", webpage_html).group()
        except Exception as e:
            self.logger.error(e) # NOTE: Again does this even raise an exception and should we log it? ~ Goldy
            return None
        urlh = f"https://dood.to{pass_md5}"
        headers = {
            "referer": "https://dood.to",
        }
        self.http_client.add_header_elem(headers)
        res = self.http_client.get(urlh).text
        md5 = pass_md5.split("/")
        true_url = res + "MovCli3oPi?token=" + md5[-1]
        return true_url
    
    def streamwish(self, url):
        req = self.http_client.get(url).text
        file = re.findall(r'file:"(.*?)"', req)[0]
        return file
    
    def cdn(self, id: str, episode: int) -> str:
        req = self.http_client.get(self.base_url + f"/watch/{id}/watching.html?ep={episode}")
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