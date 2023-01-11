from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re

class viewasian(WebScraper):
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
    
    def check(self, data):
        try:
            if int(data) > 1:
                return "TV"
            else:
                return "MOVIE"
        except:
            return "TV"

    def results(self, data: str):
        request = self.client.get(f"{self.base_url}/movie/search/{data}")
        soup = BS(request, "lxml")
        streams = soup.findAll("a", {"class": "ml-mask jt"})
        urls = [streams[i]["href"] for i in range(len(streams))]
        title = [streams[i]["title"] for i in range(len(streams))]
        ids = [streams[i]["class"] for i in range(len(streams))]
        mov_or_tv = [self.check(streams[i].find("span", {"class": "mli-eps"}).find("i").text) for i in range(len(streams))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        request = self.client.get(f"{self.base_url}{url}")
        soup = BS(request, "lxml")
        href = soup.find("a", {"class":"bwac-btn"})["href"]
        request = self.client.get(f"{self.base_url}{href}")
        soup = BS(request, "lxml")
        episodes = soup.findAll("li", {"class": "ep-item"})
        episode = int(
                    input(
                        self.lmagenta(
                            f"Please input the episode number(Total: {len(episodes)}): "
                        )
                    )
                )
        request = self.client.get(f"{self.base_url}{href}?ep={episode}")
        soup = BS(request, "lxml")
        try:
            streamtape = soup.find("li", {"class": "streamtape"})["data-video"]
            li = self.streamtape(streamtape)
        except:
            xstreamcdn = soup.find("li", {"class": "xstreamcdn"})["data-video"]
            li = self.xstreamcdn(xstreamcdn)
        print(li)
        return li, episode
    
    def mov(self, url):
        request = self.client.get(f"{self.base_url}{url}")
        soup = BS(request, "lxml")
        href = soup.find("a", {"class":"bwac-btn"})["href"]
        request = self.client.get(f"{self.base_url}{href}?ep={1}")
        soup = BS(request, "lxml")
        li = soup.find("li", {"class": "xstreamcdn"})["data-video"]
        return li

    def streamtape(self, url):
        string = re.findall("""v\/([^"']*)\/""", url)[0]
        request = self.client.get(f"https://streamtape.com/e/{string}").text
        regex = r"""'robotlink'\)\.innerHTML = '(.*?)'\+ \('(.*?)'\)"""
        results = re.findall(regex, request)
        for tuple in results:
            url = tuple[0]
            rest = tuple[1]
        li = f"https:{url}{rest[3:]}"
        return li

    def xstreamcdn(self, url):
        self.client.set_headers({"origin": "https://fembed9hd.com", "referer": f"{url}"})
        string = re.findall("""v\/([^"']*)""", url)[0]
        request = self.client.post(f"https://fembed9hd.com/api/source/{string}", data={"r": "https://viewasian.co/", "d": "fembed9hd.com"}).json()
        file = request["data"]
        if file == "Video not found or has been removed":
            print("Video not found or has been removed")
            return
        else:
            file = request["data"][-1]["file"]
        print(file)
        return file

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode = self.ask(t[self.url])
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            print("Only Shows can be downloaded with sd")
            return
        name = m[self.title]
        url = self.mov(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)



