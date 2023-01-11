from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re

class gogoanime(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q.replace(" ", "-")
    
    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/search.html?keyword={data}")
        soup = BS(req, "lxml")
        items = soup.find("ul", {"class": "items"}).findAll("li")
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a")["title"] for i in range(len(items))]
        ids = [items[i].find("a")["title"] for i in range(len(items))]
        mov_or_tv = ["TV" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def ask(self, url):
        req = self.client.get(f"{self.base_url}{url}")
        soup = BS(req, "lxml")
        episodes = soup.find("ul", {"id": "episode_page"}).find("a")["ep_end"]
        episode = int(
            input(
                self.lmagenta(
                    f"Please input the episode number(Total: {episodes}): "
                    )
                )
            )
        url = url.split("/")[-1]
        request = self.client.get(f"{self.base_url}/{url}-episode-{episode}")
        soup = BS(request, "lxml")
        url = soup.find("li", {"class": "xstreamcdn"}).find("a")["data-video"]
        return url, episode
    
    def cdn_url(self, url):
        self.client.set_headers({"origin": "https://fembed9hd.com", "referer": f"{url}"})
        string = re.findall("""v\/([^"']*)""", url)[0]
        request = self.client.post(f"https://fembed9hd.com/api/source/{string}", data={"r": "https://www1.gogoanime.bid/", "d": "fembed9hd.com"}).json()
        file = request["data"]
        if file == "Video not found or has been removed":
            print("Video not found or has been removed")
            exit(1)
        else:
            file = request["data"][-1]["file"]
        print(file)
        return file

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        link, episode = self.ask(t[self.url])
        url = self.cdn_url(link)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)