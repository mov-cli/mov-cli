from bs4 import BeautifulSoup as BS
from ...utils.scraper import WebScraper
from re import findall


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:80.0) Gecko/20100101 Firefox/80.0"
        }

    def search(self, q: str = None):
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q

    def results(self, q: str) -> list:
        q = q.replace(" ", "+")
        self.client.set_headers(self.headers)
        html = self.client.get(f"https://eja.tv/?search={q}").text
        soup = BS(html, self.scraper)
        col = soup.findAll("div", {"class": "col-sm-4"})
        urls = [col[i].findAll("a")[1]["href"] for i in range(len(col))]
        title = [col[i].findAll("a")[1].text for i in range(len(col))]
        ids = [col[i].findAll("a")[1]["href"].strip("?") for i in range(len(col))]
        mov_or_tv = [col[i].findAll("img")[0]["alt"] for i in range(len(col))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def get_hls(self, url):
        link = self.client.get(f"https://eja.tv/?{url}", redirects=True)
        link = link.url
        return findall("\?(.*)#", link)[0]

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.get_hls(m[self.aid])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
