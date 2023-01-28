from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re
import mov_cli.__main__ as movcli


class hentaimama(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        print("[!] Warning: This Provider contains Porn")
        goon = input("Are you Sure that you want to continue [y/n]: ")
        if goon == "y":
            pass
        else:
            return movcli.movcli()
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q
    
    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}").text
        soup = BS(req, "lxml")
        items = soup.findAll("div", {"class": "result-item"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("img")["alt"] for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["TV" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(url).text
        soup = BS(req, "lxml")
        episodes = soup.findAll("article", {"class": "item se episodes"})
        episode = int(self.askepisode(len(episodes)))
        episodes = episodes[::-1]
        url = episodes[episode - 1].find("a")["href"]
        return url, episode

    def cdn_url(self, url):
        req = self.client.get(url)
        soup = BS(req, "lxml")
        link = soup.find("div", {"id": "option-1"}).find("iframe")["src"]
        q = self.client.get(link).text
        regex = 'file: "(.*?)"'
        url = re.findall(regex, q)[0]
        return url
    
    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode = self.ask(t[self.url])
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)