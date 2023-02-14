from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re

class watchasian(WebScraper):
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
    
    def results(self, data: str):
        req = self.client.get(f"{self.base_url}/search?type=movies&keyword={data}").text
        soup = BS(req, "lxml")
        ul = soup.find("ul", {"class": "switch-block list-episode-item"}).findAll("li")
        urls = [ul[i].find("a")["href"] for i in range(len(ul))]
        title = [ul[i].find("h3").text for i in range(len(ul))]
        ids = ["1" for i in range(len(ul))]
        mov_or_tv = ["TV" for i in range(len(ul))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, "lxml")
        episodes = soup.find("ul",{"class": "list-episode-item-2 all-episode"}).findAll("li")
        episode = int(self.askepisode(len(episodes)))
        episodes = episodes[::-1]
        href = episodes[episode - 1].find("a")["href"]
        q = self.client.get(self.base_url + href).text
        soup = BS(q, "lxml")
        if re.search("doodstream", q):
            li = soup.find("li", {"class": "doodstream"})["data-video"]
        else:
            raise Exception("Unable to find URL")
        return li, episode   

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
        req = self.client.get(f"{self.base_url}{t[self.url]}").text
        soup = BS(req, "lxml")
        episodes = soup.find("ul",{"class": "list-episode-item-2 all-episode"}).findAll("li")
        episodes = episodes[::-1]
        for e in range(len(episodes)):
            href = episodes[e].find("a")["href"]
            q = self.client.get(self.base_url + href).text
            soup = BS(q, "lxml")
            if re.search("doodstream", q):
                li = soup.find("li", {"class": "doodstream"})["data-video"]
            else:
                raise Exception("Unable to find URL")
            url = self.doodstream(li)
            self.dl(url, t[self.title], episode=e+1)


    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        link, episode = self.ask(t[self.url])
        url = self.doodstream(link)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)
