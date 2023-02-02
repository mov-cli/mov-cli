from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re
import mov_cli.__main__ as movcli
from urllib.parse import unquote
from base64 import b64decode

class xxxmax(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q: str):
        print("[!] Warning: This Provider contains Porn\r\n")
        goon = input("Continue? [y/n]: ")
        if goon == "y":
            pass
        else:
            return movcli.movcli()
        q = (
            input("[!] Please Enter the name of the Porn: ")
            if q is None
            else q
        )
        return q.replace(" ", "+")
    
    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}").text
        soup = BS(req, "lxml")
        items = soup.findAll("article", {"class": "thumb-block"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a")["title"] for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def cdn_url(self, url):
        req = self.client.get(url).text
        soup = BS(req, "lxml")
        items = soup.find("div", {"class": "responsive-player"})
        iframe = items.find("iframe")["src"]
        encrypted = re.findall('q=(.*)', iframe)[0]
        decrypted = unquote(str(b64decode(encrypted)))
        url = re.findall('src="(.*?)"', decrypted)[0]
        return url
    
    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name, referrer=m[self.url])