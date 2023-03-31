from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re


class yoturkish(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}").text
        soup = BS(req, "lxml")
        items = []
        mlitem = soup.findAll("div", {"class": "item"})
        for i in range(len(mlitem)):
            if str(mlitem[i]).__contains__("episode"):
                pass
            else:
                items.append(mlitem[i])
        if soup.find_all("ul", {"class": "pagination"}):
            pagination = soup.find("ul", {"class": "pagination"}).findAll("li")[1:]
            for page in pagination:
                req = self.client.get(page.find("a")["href"]).text
                soup = BS(req, "lxml")
                pageitem = soup.findAll("div", {"class": "item"})
                for i in range(len(pageitem)):
                    if str(pageitem[i]).__contains__("episode"):
                        pass
                    else:
                        items.append(pageitem[i])
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a")["title"] for i in range(len(items))]
        ids = [items[i]["class"] for i in range(len(items))]
        mov_or_tv = ["TV" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(url, True).text
        soup = BS(req, "lxml")
        episodes = soup.findAll("a", {"class": "episod"})
        episode = int(self.askepisode(len(episodes)))
        req = self.client.get(episodes[episode - 1]["href"], True).text
        regex = r'''<iframe width="100%" height="100%" src="https:\/\/tukipasti\.com(.*?)"'''
        s = re.findall(regex, req)[0]
        req = self.client.get(f"https://tukipasti.com{s}").text
        url = re.findall("var urlPlay = '(.*?)'", req)[0]
        print(url)
        return url, episode, f"https://tukipasti.com{s}"

    def download(self, t):
        req = self.client.get(t[self.url]).text
        soup = BS(req, "lxml")
        episodes = soup.findAll("a", {"class": "episod"})
        for e in range(len(episodes)):
            req = self.client.get(episodes[e]["href"]).text
            regex = r'''<iframe width="100%" height="100%" src="https:\/\/tukipasti\.com(.*?)"'''
            s = re.findall(regex, req)[0]
            req = self.client.get(f"https://tukipasti.com{s}").text
            url = re.findall("var urlPlay = '(.*?)'", req)[0]
            print(url)
            self.dl(
                url,
                t[self.title],
                season="",
                episode=e + 1,
                referrer=f"https://tukipasti.com{s}",
            )

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd" or "ds"):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        url, episode, ref = self.ask(t[self.url])
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name, referrer=ref)
