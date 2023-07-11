import re
import importlib
import tldextract
from fzf import fzf_prompt
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS
from ...utils.scraper import WebScraper

"""
Original Code from https://github.com/edl2/sportsapi
Rewritten for mov-cli
Needs a rework
"""


class Provider(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.sport = None
        self.extractor = tldextract.TLDExtract()

    def date(self):
        return datetime.today().strftime("%Y-%m-%d")

    def search(self, q: str):
        sports = ["nba", "nfl", "mlb", "nhl", "mma", "motorsport", "cricket"]
        q = fzf_prompt(sports)
        self.sport = q
        return q

    def results(self, data: str) -> list:
        data = self.client.get(
            f"https://sportscentral.io/api/{data}-tournaments?date={self.date()}"
        ).json()
        urls = [
            match["name"]
            for tournament in data
            for match in tournament["events"]
            if match["status"]["type"] == "inprogress"
        ]
        title = [
            match["name"]
            for tournament in data
            for match in tournament["events"]
            if match["status"]["type"] == "inprogress"
        ]
        ids = [
            match["id"]
            for tournament in data
            for match in tournament["events"]
            if match["status"]["type"] == "inprogress"
        ]
        mov_or_tv = [
            "match"
            for tournament in data
            for match in tournament["events"]
            if match["status"]["type"] == "inprogress"
        ]
        if not ids:
            raise Exception("No Match was Found that is in progress.")
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def cdn_url(self, id):
        req = self.client.get(
            f"https://scdn.dev/main-assets/{id}/{self.sport}?origin=sportsurge.club&="
        )
        soup = BS(req, self.scraper)
        print(soup.prettify())
        ts = []
        tr = soup.find("tbody").find_all("tr")  #
        for i in range(len(tr)):
            h = self.client.get(tr[i].find("a")["href"]).text
            try:
                url = re.findall('window.location.href = "(.*?)";', h)[0]
            except IndexError:
                url = "https://github.com"
            A = urlparse(url).netloc
            urls = [
                "weakstream.org",
                "fabtech.work",
                "allsportsdaily.co",
                "techclips.net",
                "gameshdlive.xyz",
                "enjoy4hd.site" "motornews.live",
                "cr7sports.us",
                "com.methstreams.site",
                "1stream.eu",
                "www.techstips.info",
                "poscitech.org",
                "poscitech.com",
                "en.ripplestream4u.online",
                "rainostreams.com",
                "livestreames.us",
                "onionstream.live",
            ]
            if A in urls:
                ts.append(tr)
        else:
            pass
        channels = [ts[0][i].find("b").text for i in range(len(ts))]
        watch_urls = [ts[0][i].find("a")["href"] for i in range(len(ts))]
        res = [ts[0][i].find("td").text for i in range(len(ts))]
        stuff = [list(sublist) for sublist in zip(channels, watch_urls, res)]
        ask = []
        print(ts)
        for ix, vl in enumerate(stuff):
            ask.append(f"[{ix + 1}] {vl[self.title]} {vl[2]}")
        pre = fzf_prompt(ask)
        choice = re.findall(r"\[(.*?)\]", pre)[0]
        url = stuff[int(choice) - 1][self.url]
        h = self.client.get(url).text
        url = re.findall('window.location.href = "(.*?)";', h)[0]
        A = urlparse(url).netloc
        extracted_url = self.extractor(A).domain
        try:
            get_link = importlib.import_module(
                f"..extractors.scdn.{extracted_url}.get_link"
            )
        except ImportError:
            from ...extractors.scdn.ripple import get_link

        m3u8 = get_link(url)
        return m3u8, A

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url, domain = self.cdn_url(m[self.aid])
        if state == "d":
            self.dl(url, name, referrer=f"https://{domain}/")
            return
        self.play(url, name, referrer=f"https://{domain}/")
