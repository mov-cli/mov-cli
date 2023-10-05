from __future__ import annotations
from typing import TYPE_CHECKING

from ..media import Metadata, MetadataType, Series, Movie

if TYPE_CHECKING:
    from typing import List, Dict
    from ..config import Config
    from bs4 import BeautifulSoup
    from ..http_client import HTTPClient

import re
from ..scraper import Scraper

__all__ = ("Gogoanime",)

class Gogoanime(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://gogoanimehd.io"
        super().__init__(config, http_client)

    def search(self, query: str, limit: int = 10) -> List[Metadata]:
        query = query.replace(' ', '-')
        results = self.__results(query, limit)
        return results    

    def __results(self, query: str, limit: int = None) -> List[Metadata]:
        metadata_list = []
        pagination = 1

        while True:
            req = self.http_client.get(f"{self.base_url}/search.html?keyword={query}&page={pagination}")
            soup = self.soup(req)
            items = soup.find("ul", {"class": "items"}).findAll("li")

            if len(items) == 0:
                break

            for item in items:
                item: BeautifulSoup

                id = item.find("a")["href"].split("/")[-1]
                title = item.find("a")["title"]
                img = item.find("img")["src"]
                year = item.find("p", {"class": "released"}).text.split()[-1]

                page = self.http_client.get(self.base_url + f"/category/{id}")
                _soup = self.soup(page)

                episode_page = _soup.find("ul", {"id": "episode_page"})
                li = episode_page.findAll("li")
                last = li[-1].find("a")["ep_end"]

                if last == "1":
                    type = MetadataType.MOVIE
                else:
                    type = MetadataType.SERIES

                info_body = _soup.find("div", {"class": "anime_info_body_bg"})

                _p = info_body.findAll("p")

                description = [str.strip(x) for x in _p[2].strings if str.strip(x) != ''][1].replace(r"\r\n", "\r\n")

                genres = _p[3].findAll("a")
                genres = [i.text.split(" ")[-1] for i in genres]

                metadata_list.append(
                    Metadata(
                        title = title,
                        id = id,
                        url = self.base_url + f"/category/{id}",
                        type = type,
                        image_url = img,
                        year = year,
                        genre = genres,
                        description = description
                    )
                )

                if len(metadata_list) == limit:
                    break

            pagination += 1

        return metadata_list

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int, int]:
        page = self.http_client.get(f"https://gogoanimehd.io/category/{metadata.id}")
        _soup = self.soup(page)

        episode_page = _soup.find("ul", {"id": "episode_page"})
        li = episode_page.findAll("li")
        last = int(li[-1].find("a")["ep_end"])
        return {1: last} # TODO: Return multiple seasons.

    def __cdn(self, id, episode):
        req = self.http_client.get(self.base_url + f"/{id}-episode-{episode}")
        soup = self.soup(req)
        dood = soup.find("li", {"class": "doodstream"}).find("a")["data-video"]
        url = self.__dood(dood)
        if not url:
            streamwish = soup.find("li", {"class": "streamwish"}).find("a")["data-video"]
            url = self.__streamwish(streamwish)
        return url

    def scrape(self, metadata: Metadata, episode: int = None) -> Series | Movie:
        if episode is None or metadata.type == MetadataType.MOVIE:
            episode = 1

        url = self.__cdn(metadata.id, episode)

        if metadata.type == MetadataType.MOVIE:
            return Movie(
                url,
                title = metadata.title,
                referrer = self.base_url,
                year = metadata.year,
                subtitles = None
            )

        return Series(
            url,
            title = metadata.title,
            referrer = self.base_url,
            episode = episode,
            season = 1,
            subtitles = None
        )

    def __dood(self, url):
        video_id = url.split("/")[-1]
        webpage_html = self.http_client.get(
            f"https://dood.to/e/{video_id}", redirect = True
        )
        webpage_html = webpage_html.text
        try:
            pass_md5 = re.search(r"/pass_md5/[^']*", webpage_html).group()
        except Exception as e:
            self.logger.error(e) # NOTE: Does this even raise an exception and should we log it? ~ Goldy
            return None
        urlh = f"https://dood.to{pass_md5}"
        res = self.http_client.get(urlh, headers = {"referer": "https://dood.to"}).text
        md5 = pass_md5.split("/")
        true_url = res + "MovCli3oPi?token=" + md5[-1]
        return true_url
    
    def __streamwish(self, url):
        req = self.http_client.get(url).text
        file = re.findall(r'file:"(.*?)"', req)[0]
        return file