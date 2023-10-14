from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from typing import List, Dict, Tuple
   from ..config import Config
   from bs4 import Tag
   from ..http_client import HTTPClient

import re
from ..media import Metadata, Series
from .. import utils
from ..scraper import Scraper, MediaNotFound

__all__ = ("ViewAsian",)

class ViewAsian(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://viewasian.co"
        super().__init__(config, http_client)

    def __search(self, metadata: Metadata, limit: int = None) -> List[Tuple[str, str]]:
        id_list = []

        search_title = metadata.title.replace(" ", "-")

        page = 0

        while True:
            page += 1
            response = self.http_client.get(f"{self.base_url}/movie/search/{search_title}?page={page}")

            soup = self.soup(response)

            items: List[Tag] = soup.findAll("a", {"class": "ml-mask"})

            if len(items) == 0:
                break

            for item in items:
                title = item["title"]
                id = item["href"].split("/")[-1]

                id_list.append((id, title))

                if len(id_list) == limit:
                    break

        return id_list

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        results = self.__search(metadata, 1)

        if results == []:
            raise MediaNotFound("No search results were found!", self)

        id, name = results[0]
        req = self.http_client.get(self.base_url + f"/watch/{id}/watching.html")
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
        res = self.http_client.get(urlh, headers = {"referer": "https://dood.to"}).text
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

    def scrape(self, metadata: Metadata, limit: int = 10, episode: utils.EpisodeSelector = None) -> Series:
        results = self.__search(metadata, limit)

        if results == []:
            raise MediaNotFound("No search results were found!", self)

        id, name = results[0]

        if episode is None:
            episode = utils.EpisodeSelector()

        url, referrer = self.cdn(id, episode)

        return Series(
            url = url,
            title = metadata.title,
            referrer = referrer,
            episode = episode,
            season = None,
            subtitles = None
        )