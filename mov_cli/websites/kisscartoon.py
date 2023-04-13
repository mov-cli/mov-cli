from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re
import httpx

cdn_url_re = r"/\\\/cdn\\\/hls\\\/([a-fA-F\d]{32})\\\/master\.txt/gm"


class kisscartoon(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str = None) -> str:
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q

    def results(self, q):
        res = self.client.get(f"{self.base_url}/?s={q}")
        soup = BS(res.text, "lxml")
        cartoon_name = [i.text for i in soup.select("div.title > a")]
        urls = [i["href"] for i in soup.select("div.title > a")]
        discrim = [httpx.URL(i).path for i in urls]
        mov_or_tv = [
            i.text for i in soup.select("div.thumbnail.animation-2 > a > span")
        ]
        return [
            list(sublist) for sublist in zip(cartoon_name, urls, discrim, mov_or_tv)
        ]

    def ask(self, url):
        res = httpx.get(url).text
        soup = BS(res, "lxml")
        season_id = httpx.URL(soup.find("link", {"rel": "shortlink"})["href"]).params[
            "p"
        ]
        print(season_id)
        try:
            last_page = soup.select("ul.episode_list > li")[-1].text
        except IndexError:
            last_page = 0
        self.client.add_elem({"referer": url})
        self.client.add_elem({"x-requested-with": "XMLHttpRequest"})
        num_eps = BS(
            self.client.get(
                f"https://thekisscartoon.com/ajax-episode/?page_sele={last_page}&id={season_id}"
            ).text,
            "lxml",
        )
        num_eps = num_eps.select("div.numerando")[-1].text
        episode = int(self.askepisode(int(num_eps)))
        url = url.strip("/")
        url = f"{url}-episode-{episode}/".replace("tvshows", "episode")
        return url, episode

    def cdn_url(self, url):
        res = self.client.get(url).text
        film_id = re.findall('filmId = "(.*?)"', res)[0]
        self.client.add_elem({"Referer": url})
        self.client.add_elem({"x-requested-with": "XMLHttpRequest"})
        inter_1 = self.client.get(
            f"{self.base_url}/ajax-get-link-stream/?server=fembed&filmId={film_id}"
        ).text
        if inter_1 == "":
            inter_1 = self.client.get(
                f"{self.base_url}/ajax-get-link-stream/?server=streamango&filmId={film_id}"
            ).text
        self.client.add_elem({"Referer": self.base_url})
        inter_2 = self.client.get(inter_1).text
        hls = re.findall("\\\/cdn\\\/hls\\\/([a-fA-F\d]*)\\\/master\.txt", inter_2)[0]
        videoServer = re.findall('"videoServer":"(.*?)"', inter_2)[0]
        hls = (
            "https://comedyshow.to"
            + "/cdn/hls/"
            + hls
            + "/master.txt"
            + "?s="
            + videoServer
            + "&d="
        )
        print(hls)
        return hls, inter_1

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.download(t)
            return
        name = t[self.title]
        link, episode = self.ask(t[self.url])
        url, ref = self.cdn_url(link)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name, referrer=ref)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url, ref = self.cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        if state == "sd":
            print("You can download only Shows with 'sd'")
            return
        self.play(url, name, referrer=ref)
