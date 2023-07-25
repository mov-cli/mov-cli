from ...utils.scraper import WebScraper
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
        req = self.client.get(f"{self.base_url}/?s={data}").text
        soup = BS(req, self.scraper)
        mlitem = soup.findAll("div", {"class": "ml-item"})
        items = []
        for i in range(len(mlitem)):
            if str(mlitem[i]).__contains__("episode"):
                pass
            else:
                items.append(mlitem[i])
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a")["oldtitle"] for i in range(len(items))]
        ids = [items[i]["class"] for i in range(len(items))]
        mov_or_tv = ["TV" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(url).text
        soup = BS(req, self.scraper)
        episodes = soup.findAll("a", {"class": "episodi"})
        episode = int(self.askepisode(len(episodes)))
        req = self.client.get(episodes[episode - 1]["href"]).text
        url, tukibase = self.tuki(req)
        return url, episode, tukibase

    def download(self, t):
        req = self.client.get(t[self.url]).text
        soup = BS(req, self.scraper)
        episodes = soup.findAll("a", {"class": "episodi"})
        for e in range(len(episodes)):
            req = self.client.get(episodes[e]["href"]).text
            url, tukibase = self.tuki(req)
            print(url)
            self.dl(
                url,
                t[self.title],
                season="",
                episode=e + 1,
                referrer=tukibase,
            )

    def TV_PandDP(self, t: list, state: str):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        url, episode, ref = self.ask(t[self.url])
        if state == "d":
            self.dl(url, name, episode=episode)
            return
        self.play(url, name, referrer=ref)
