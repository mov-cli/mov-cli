from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re

class kimcartoon(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q
    
    def results(self, q):
        res = self.client.post(f"{self.base_url}/Search/Cartoon", data={"keyword": q})
        soup = BS(res.text, "lxml")
        div = soup.find("div", {"class": "list-cartoon"})
        cartoons = div.findAll("div", {"class": "item"})
        title = [cartoons[i].find("span").text for i in range(len(cartoons))]
        urls = [cartoons[i].find("a")["href"] for i in range(len(cartoons))]
        ids = [i for i in range(len(cartoons))]
        mov_or_tv = ["TV" if cartoons[i].find("a")["href"].__contains__("Season") else "MOVIE" for i in range(len(cartoons))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        res = self.client.get(self.base_url + url)
        soup = BS(res, "lxml")
        table = soup.find("table", {"class": "listing"})
        episodes = table.findAll("a", {"rel": "noreferrer noopener"})
        episode = int(
            input(
                self.lmagenta(
                    f"Please input the episode number:{len(episodes)}: "
                )
            )
        )
        url = episodes[len(episodes) - episode]["href"]
        return url, episode
    
    def download(self, t: list):
        res = self.client.get(self.base_url + t[self.url])
        soup = BS(res, "lxml")
        table = soup.find("table", {"class": "listing"})
        episodes = table.findAll("a", {"rel": "noreferrer noopener"})
        for e in range(len(episodes)):
            epi = e + 1
            link = episodes[len(episodes) - epi]["href"]
            url = self.cdn_url(link)
            self.dl(url, t[self.title], episode=e + 1)
    
    def cdn_url(self, url):
        res = self.client.get(self.base_url + url).text
        iframe_id = re.findall('''src="https://www.luxubu.review/v/(.*?)"''',res)[0]
        r= self.client.post(f"https://www.luxubu.review/api/source/{iframe_id}", data=None).json()['data']
        return r[-1]["file"]
    
    def movtable(self, url):
        res = self.client.get(self.base_url + url)
        soup = BS(res, "lxml")
        table = soup.find("table", {"class": "listing"})
        url = table.findAll("a", {"rel": "noreferrer noopener"})[0]["href"]
        return url
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

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            print("Only Shows can be downloaded with sd")
            return
        name = m[self.title]
        link = self.movtable(f"{m[self.url]}")
        url = self.cdn_url(link)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)



