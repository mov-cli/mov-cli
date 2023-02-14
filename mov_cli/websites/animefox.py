from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re

class animefox(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        q = (
            input("[!] Please Enter the name of the Movie: ")
            if q is None
            else q
        )
        return q.replace(" ", "+")
    
    def results(self, data: str) -> list:
        req = self.client.get(f"https://animefox.to/search?keyword={data}")
        soup = BS(req, "lxml")
        items = soup.findAll("a", {"class": "film-poster-ahref"})
        urls = [items[i]["href"] for i in range(len(items))]
        title = [items[i]["title"] for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" if items[i].__contains__("Movie") else "TV" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        a = self.client.get(f"{self.base_url}{url}")
        soup = BS(a, "lxml")
        url = soup.find("div", {"class": "film-buttons"}).find("a")["href"]
        req = self.client.get(self.base_url + url)
        soup = BS(req, "lxml")
        episodes = len(soup.find("div", {"id": "episodes-page-1"}).findAll("a"))
        episode = self.askepisode(episodes)
        return self.base_url + url[:-1] + episode, episode

    def mov(self, url):
        a = self.client.get(f"{self.base_url}{url}")
        soup = BS(a, "lxml")
        url = soup.find("div", {"class": "film-buttons"}).find("a")["href"]
        return self.base_url + url

    def cdn_url(self, url):
        req = self.client.get(url)
        soup = BS(req, "lxml")
        goload = soup.find("select", {"id": "select-iframe-to-display"}).findAll("option")[-1]["value"]
        url = f"https://{goload}".split("-")[0]
        a = self.client.head(url, redirects=False).headers["location"]
        a = self.client.get(a)
        soup = BS(a, "lxml")
        server = []
        servers = soup.findAll("li", {"class": "linkserver"})
        for video in servers:
            if "dood.wf" in str(video["data-video"]):
                server.append(video["data-video"])
        return self.doodstream(server[0])
        
    def doodstream(self, url):
        domain = re.findall("""([^"']*)\/e""", url)[0]
        req = self.client.get(url).text
        pass_md = re.findall(r"/pass_md5/[^']*", req)[0]
        token = pass_md.split("/")[-1]
        self.client.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Referer": f"{url}", "Accept-Language": "en-GB,en;q=0.5"})
        drylink = self.client.get(f"{domain}{pass_md}").text
        streamlink = f"{drylink}zUEJeL3mUN?token={token}"
        print(streamlink)
        return streamlink
    
    def download(self, t):
        a = self.client.get(f"{self.base_url}{t[self.url]}")
        soup = BS(a, "lxml")
        url = soup.find("div", {"class": "film-buttons"}).find("a")["href"]
        req = self.client.get(self.base_url + url)
        soup = BS(req, "lxml")
        episodes = len(soup.find("div", {"id": "episodes-page-1"}).findAll("a"))
        for e in range(episodes):
            url = self.cdn_url(self.base_url + url[:-1] + e+1)
            self.dl(url, name=t[self.title], episode=e+1)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        link, episode = self.ask(t[self.url])
        url = self.cdn_url(link)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)

    def MOV_PandDP(self, t: list, state: str = "d" or "p"):
        name = t[self.title]
        link = self.mov(t[self.url])
        url = self.cdn_url(link)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)