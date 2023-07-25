from bs4 import BeautifulSoup as BS
from ...utils.scraper import WebScraper
import re


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "-")

    def results(self, data: str):
        request = self.client.get(f"{self.base_url}/movie/search/{data}")
        soup = BS(request, self.scraper)
        streams = soup.findAll("a", {"class": "ml-mask jt"})
        urls = [streams[i]["href"] for i in range(len(streams))]
        title = [streams[i]["title"] for i in range(len(streams))]
        ids = [streams[i]["class"] for i in range(len(streams))]
        mov_or_tv = ["TV" for i in range(len(streams))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        request = self.client.get(f"{self.base_url}{url}")
        soup = BS(request, self.scraper)
        href = soup.find("a", {"class": "bwac-btn"})["href"]
        request = self.client.get(f"{self.base_url}{href}")
        soup = BS(request, self.scraper)
        episodes = soup.findAll("li", {"class": "ep-item"})
        episode = int(self.askepisode(len(episodes)))
        request = self.client.get(f"{self.base_url}{href}?ep={episode}").text
        soup = BS(request, self.scraper)
        if re.search("doodstream", request):
            dood = soup.find("li", {"class": "doodstream"})["data-video"]
            li = self.doodstream(dood)
        elif re.search("streamtape", request):
            streamtape = soup.find("li", {"class": "streamtape"})["data-video"]
            li = self.streamtape(streamtape)
        else:
            raise Exception("Unable to find URL")
        return li, episode

    def streamtape(self, url):
        string = re.findall("""v\/([^"']*)\/""", url)[0]
        request = self.client.get(f"https://streamtape.com/e/{string}").text
        if '<h1 class="white">Video not found!</h1>' not in request:
            regex = r"""'robotlink'\)\.innerHTML = '(.*?)'\+ \('(.*?)'\)"""
            results = re.findall(regex, request)
            for tuple in results:
                url = tuple[0]
                rest = tuple[1]
            li = f"https:{url}{rest[3:]}"
            return li
        raise Exception("Video not found or removed")

    def download(self, t):
        request = self.client.get(f"{self.base_url}{t[self.url]}")
        soup = BS(request, self.scraper)
        href = soup.find("a", {"class": "bwac-btn"})["href"]
        request = self.client.get(f"{self.base_url}{href}")
        soup = BS(request, self.scraper)
        episodes = soup.findAll("li", {"class": "ep-item"})
        for e in range(len(episodes)):
            request = self.client.get(f"{self.base_url}{href}?ep={e+1}").text
            soup = BS(request, self.scraper)
            if re.search("doodstream", request):
                dood = soup.find("li", {"class": "doodstream"})["data-video"]
                li = self.doodstream(dood)
            elif re.search("streamtape", request):
                streamtape = soup.find("li", {"class": "streamtape"})["data-video"]
                li = self.streamtape(streamtape)
            else:
                raise Exception("Unable to find URL")
            self.dl(li, t[self.title], episode=e + 1)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        url, episode = self.ask(t[self.url])
        if state == "d":
            self.dl(url, name, episode=episode)
            return
        self.play(url, name)
