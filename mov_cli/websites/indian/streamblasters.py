from ...utils.scraper import WebScraper
from ...utils.props import NoSupportedProvider

from bs4 import BeautifulSoup as BS
import re


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str = None) -> str:
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}")
        soup = BS(req, self.scraper)
        items = soup.findAll("div", {"class": "title"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a").text for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def doodext(self, url):
        req = self.client.get(url).text
        soup = BS(req, self.scraper)
        ply = soup.find("li", {"id": "player-option-1"})
        post = ply["data-post"]
        self.client.set_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
                "Referer": f"{url}",
                "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            }
        )
        data = {"action": "doo_player_ajax", "post": post, "nume": "1", "type": "movie"}
        post = self.client.post(
            f"{self.base_url}/wp-admin/admin-ajax.php", data=data
        ).text
        try:
            src = re.findall('''"https:(.*?)"''', post)[0].replace("\/", "/")
        except:
            raise NoSupportedProvider
        if "\\" in src:
            src = src.replace("\\", "")
        src = f"https:{src}"
        print(src)
        return src

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.doodext(m[self.url])
        url = self.doodstream(url)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
