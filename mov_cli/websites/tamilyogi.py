from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re

class tamilyogi(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q: str):
        q = (
            input("[!] Please Enter the name of the Movie: ")
            if q is None
            else q
        )
        return q
    
    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}").text
        soup = BS(req, "lxml")
        items = soup.findAll("div", {"class": "cover"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a")["title"] for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def cdn_url(self, url):
        req = self.client.get(url).text
        soup = BS(req, "lxml")
        iframe = soup.find("iframe")["src"]
        q = self.client.get(iframe).text
        url = re.findall('file:"(.*?)"', q)[0]
        return url
    
    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
