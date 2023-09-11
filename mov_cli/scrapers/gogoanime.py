from __future__ import annotations
from typing import TYPE_CHECKING

from ..media import Metadata, MetadataType, Series, Movie

if TYPE_CHECKING:
    from typing import List
    from ..config import Config
    from bs4 import BeautifulSoup

from ..scraper import Scraper
import re

class gogoanime(Scraper):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://gogoanimehd.io"
        super().__init__(config)

    def search(self, query: str) -> List[Metadata]:
        query = query.replace(' ', '-')
        results = self.__results(query)
        return results    

    def __results(self, query: str) -> List[Metadata]:
        metadata_list = []
        pagination = 1
        while True:
            req = self.get(f"{self.base_url}/search.html?keyword={query}&page={pagination}")
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
                
                page = self.get(f"https://gogoanimehd.io/category/{id}")
                _soup = self.soup(page)

                episode_page = _soup.find("ul", {"id": "episode_page"})
                li = episode_page.findAll("li")
                last = li[-1].find("a")["ep_end"]
                print(last)
                seasons = {}
                seasons[1] = last
                
                anime_info = _soup.find("div", {"class": "anime_info_body_bg"})
                anime_info_p = anime_info.findAll("p")[1]
                anime_info_p_type = anime_info_p.find("a")["title"]
                
                if anime_info_p_type == "Movie":
                    type = MetadataType.MOVIE
                    seasons = None
                else:
                    type = MetadataType.SERIES
            
                metadata_list.append(Metadata(
                    title = title,
                    id = id,
                    type = type,
                    image_url = img,
                    seasons = seasons,
                    year = year
                ))
            pagination += 1
        
        return metadata_list

    def cdn(self, id, episode):
        req = self.get(self.base_url + f"/{id}-episode-{episode}")
        soup = self.soup(req)
        dood = soup.find("li", {"class": "doodstream"}).find("a")["data-video"]
        url = self.dood(dood)
        if not url:
            streamwish = soup.find("li", {"class": "streamwish"}).find("a")["data-video"]
            url = self.streamwish(streamwish)
        return url

    def scrape(self, metadata: Metadata, episode: int = None) -> Series | Movie:
        if metadata.type == MetadataType.MOVIE:
            episode = 1
        
        url = self.cdn(metadata.id, episode)
        
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
        print(req)
        file = re.findall(r'file:"(.*?)"', req)[0]
        return file