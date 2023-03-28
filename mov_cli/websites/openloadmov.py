from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper


class openloadmov(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.getvid = "https://hlspanel.xyz/player/index.php?data={}&do=getVideo"

    def search(self, q: str):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}")
        soup = BS(req, "lxml")
        items = soup.findAll("div", {"class": "result-item"})
        title = [items[i].find("img")["alt"] for i in range(len(items))]
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = [
            "MOVIE" if items[i].find("span").text.__contains__("Movie") else "TV"
            for i in range(len(items))
        ]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(url)
        soup = BS(req, "lxml")
        seasons = soup.findAll("div", {"class": "se-c"})
        season = int(self.askseason(len(seasons)))
        se_c = seasons[season - 1]
        episodes = se_c.find("ul").findAll("li")
        episode = int(self.askepisode(len(episodes)))
        ep = episodes[episode - 1].find("a")["href"]
        return ep, episode, season

    def cdn_url(self, url):
        req = self.client.get(url)
        soup = BS(req, "lxml")
        iframe = soup.find("iframe")["src"]
        vidhash = iframe.split("/")[-1]
        self.client.set_headers({"x-requested-with": "XMLHttpRequest"})
        awd = self.client.post(
            self.getvid.format(vidhash),
            data={"hash": vidhash, "r": self.base_url + "/"},
        ).json()["securedLink"]
        print(awd)
        return awd

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode, season = self.ask(t[self.url])
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name, season=season, episode=episode)
            return
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url = self.cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
