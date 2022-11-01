import httpx
from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re


class ustvgo(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def lcheck(self, sender, x):
        try:
            return sender[x].find("a")["href"]
        except:
            return

    def tcheck(self, sender, x):
        try:
            return sender[x].find("a").text
        except:
            return

    def results(self, q):
        res = self.client.get(self.base_url)
        soup = BS(res, "lxml")
        sender = soup.findAll("strong")
        title = [self.tcheck(sender, i) for i in range(len(sender))]
        id = [i for i in range(len(sender) - 3)]
        url = [self.lcheck(sender, i) for i in range(len(sender))]
        channel = ["channel" for i in range(len(sender)  - 3)]
        return [list(sublist) for sublist in zip(title, url, id, channel)]
    
    def streamlink(self, uri):
        res = self.client.get(uri)
        soup = BS(res, "lxml")
        div = soup.find("div", {"class": "iframe-container"})
        url = div.find("iframe")["src"]
        self.client.set_headers({"Referer": f"{uri}"})
        res = self.client.get(f"https://ustvgo.tv{url}")
        soup = BS(res, "lxml")
        script = soup.findAll("script", {"type": "text/javascript"})[1]
        script = "".join(script)
        uri = re.findall("""hls_src='([^"']*)';""", script)[0]
        print(uri)
        return uri

    
    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url = self.streamlink(f"{m[self.url]}")
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)


    def SandR(self, q: str = None):
        return self.results(q)
