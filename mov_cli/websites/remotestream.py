from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re


class RemoteStream(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.movdb = "https://www.themoviedb.org"

    def search(self, q: str):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q

    def results(self, data: str) -> list:
        title = []
        urls = []
        ids = []
        mov_or_tv = []
        tv = self.client.get(self.movdb + f"/search/tv?query={data}&language=en").text
        movie = self.client.get(
            self.movdb + f"/search/movie?query={data}&language=en"
        ).text
        # MOVIE
        soupm = BS(movie, "lxml")
        mcards = soupm.findAll("div", {"class": "card v4 tight"})
        if mcards is not []:
            title.extend([mcards[i].find("h2").text for i in range(len(mcards))])
            print(title)
            urls.extend(["" for i in range(len(mcards))])
            ids.extend(
                [
                    mcards[i].find("a")["href"].split("/")[-1].split("?")[0]
                    for i in range(len(mcards))
                ]
            )
            mov_or_tv.extend(["MOVIE" for i in range(len(mcards))])
        soups = BS(tv, "lxml")
        scards = soups.findAll("div", {"class": "card v4 tight"})
        if scards is not []:
            title.extend([scards[i].find("h2").text for i in range(len(scards))])
            urls.extend(["" for i in range(len(scards))])
            ids.extend(
                [
                    scards[i].find("a")["href"].split("/")[-1].split("?")[0]
                    for i in range(len(scards))
                ]
            )
            mov_or_tv.extend(["TV" for i in range(len(scards))])
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, id):
        rlurl = self.client.head(f"{self.movdb}/tv/{id}", redirects=True).url
        res = self.client.get(f"{rlurl}/seasons")
        soup = BS(res, "lxml")
        seasons = soup.findAll("div", {"class": "season"})
        s = []
        for season in seasons:
            title = season.find("h2").find("a").text
            if title == "Extras":
                continue
            elif title == "Specials":
                continue
            else:
                s.append(season)
        season = self.askseason(len(s))
        req = self.client.get(f"{rlurl}/season/{season}").text
        soup = BS(req, "lxml")
        episodes = soup.find("h3", {"class": "episode_sort"}).find("span").text
        episode = self.askepisode(int(episodes))
        return season, episode

    def cdn_url(self, id=None, season=None, episode=None):
        if season is None:
            res = self.client.get(f"{self.base_url}/e/?tmdb={id}").text
        else:
            res = self.client.get(
                f"{self.base_url}/e/?tmdb={id}&s={season}&e={episode}"
            ).text
        file = re.findall('"file":"(.*?)"', res)[0]
        return file

    def sd(self, name, id):
        rlurl = self.client.head(f"{self.movdb}/tv/{id}", redirects=True).url
        res = self.client.get(f"{rlurl}/seasons")
        soup = BS(res, "lxml")
        seasons = soup.findAll("div", {"class": "season"})
        for s in range(len(seasons)):
            title = seasons[s].find("h2").find("a").text
            if title == "Extras":
                pass
            else:
                req = self.client.get(f"{rlurl}/season/{s+1}").text
                soup = BS(req, "lxml")
                episodes = soup.find("h3", {"class": "episode_sort"}).find("span").text
                for e in range(int(episodes)):
                    url = self.cdn_url(id, s + 1, e + 1)
                    self.dl(url, name, season=s + 1, episode=e + 1)

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.cdn_url(m[self.aid])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.sd(t[self.title], t[self.aid])
            return
        name = t[self.title]
        season, episode = self.ask(t[self.aid])
        url = self.cdn_url(t[self.aid], season, episode)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)
