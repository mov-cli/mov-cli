from bs4 import BeautifulSoup as BS
from ...utils.scraper import WebScraper
import re
from ...utils.props import SelectedNotAvailable


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.movdb = "https://www.themoviedb.org"
        self.dseasonp = False
        self.dshowp = True

    def search(self, q: str):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q

    def results(self, data: str) -> list:
        title = []
        urls = []
        ids = []
        mov_or_tv = []
        for i in range(2):
            if i == 0:
                get = "movie"
            else:
                get = "tv"
            req = self.client.get(
                self.movdb + f"/search/{get}?query={data}&language=en"
            ).text
            soup = BS(req, self.scraper)
            cards = soup.findAll("div", {"class": "card v4 tight"})
            if cards is not []:
                title.extend([cards[i].find("h2").text for i in range(len(cards))])
                urls.extend(["" for i in range(len(cards))])
                ids.extend(
                    [
                        cards[i].find("a")["href"].split("/")[-1].split("?")[0]
                        for i in range(len(cards))
                    ]
                )
                mov_or_tv.extend([get.upper() for i in range(len(cards))])
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, id):
        rlurl = self.client.head(f"{self.movdb}/tv/{id}", redirects=True).url
        res = self.client.get(f"{rlurl}/seasons")
        soup = BS(res, self.scraper)
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
        soup = BS(req, self.scraper)
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
        try:
            file = re.findall('"file":"(.*?)"', res)[0]
        except IndexError as e:
            raise SelectedNotAvailable
        return file

    def sd(self, name, id):
        rlurl = self.client.head(f"{self.movdb}/tv/{id}", redirects=True).url
        res = self.client.get(f"{rlurl}/seasons")
        soup = BS(res, self.scraper)
        seasons = soup.findAll("div", {"class": "season"})
        for s in range(len(seasons)):
            title = seasons[s].find("h2").find("a").text
            if title == "Extras":
                pass
            else:
                req = self.client.get(f"{rlurl}/season/{s+1}").text
                soup = BS(req, self.scraper)
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

    def TV_PandDP(self, t: list, state: str):
        if state == "s":
            self.sd(t[self.title], t[self.aid])
            return
        name = t[self.title]
        season, episode = self.ask(t[self.aid])
        url = self.cdn_url(t[self.aid], season, episode)
        if state == "d":
            self.dl(url, name, season=season, episode=episode)
            return
        self.play(url, name)
