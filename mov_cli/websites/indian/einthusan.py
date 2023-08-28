from ...utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re
from fzf import fzf_prompt


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str = None) -> str:
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        lang = [
            "tamil",
            "hindi",
            "telugu",
            "malayalam",
            "kannada",
            "bengali",
            "marathi",
            "punjabi",
        ]
        lang = fzf_prompt(lang)
        req = self.client.get(
            f"{self.base_url}/movie/results/?lang={lang}&query={data}"
        )
        soup = BS(req, self.scraper)
        items = soup.findAll("div", {"class": "block2"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [
            items[i].find("h3").text + " | " + items[i].find("span").text + " | " + str(items[i].find("div", {"class": "info"}).find("p")).split("<p>")[1].split("<span>")[0]
            for i in range(len(items))
        ]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def cdn_url(self, url):
        domain = "https://cdn4.einthusan.io"
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, self.scraper)
        etv = soup.find("section", {"id": "UIVideoPlayer"})["data-mp4-link"].replace(
            "amp;", ""
        )
        etv = re.findall(r"https:\/\/[^a-z]+(.*)", etv)[0]
        url = f"{domain}/{etv}"
        print(url)
        return url

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url = self.cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
