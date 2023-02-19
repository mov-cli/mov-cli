from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime
from fzf import fzf_prompt
from urllib.parse import urlparse
"""
Original Code from https://github.com/edl2/sportsapi
Rewritten for mov-cli
"""

class scdn(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.sport = None

    def date(self):
        return datetime.today().strftime("%Y-%m-%d")

    def search(self, q: str):
        sports = ["nba", "nfl", "mlb", "nhl", "mma", "motorsport", "cricket"]
        q = fzf_prompt(sports)
        self.sport = q
        return q
    
    def results(self, data: str) -> list:
        data = self.client.get(f"https://sportscentral.io/api/{data}-tournaments?date={self.date()}").json()
        urls = [match["name"] for tournament in data for match in tournament["events"] if match["status"]["type"] == "inprogress"]
        title = [match["name"] for tournament in data for match in tournament["events"] if match["status"]["type"] == "inprogress"]
        ids = [match["id"] for tournament in data for match in tournament["events"] if match["status"]["type"] == "inprogress"]
        mov_or_tv = ["match" for tournament in data for match in tournament["events"] if match["status"]["type"] == "inprogress"]
        if ids == []:
            raise Exception("No Match was Found that is in progress.")
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def cdn_url(self, id):
        req = self.client.get(f"https://scdn.dev/main-assets/{id}/{self.sport}?origin=sportsurge.club&=")
        soup = BS(req, "lxml")
        print(soup.prettify())
        ts = [] 
        tr = soup.find("tbody").find_all("tr")#
        for i in range(len(tr)):
            h = self.client.get(tr[i].find("a")["href"]).text
            try:
                url = re.findall('window.location.href = "(.*?)";', h)[0]
            except IndexError:
                url = "https://github.com"
            A = urlparse(url).netloc
            if A == "weakstream.org":ts.append(tr)
            elif A == "fabtech.work":ts.append(tr)
            elif A == "allsportsdaily.co":ts.append(tr)
            elif A == "techclips.net":ts.append(tr)
            elif A == "gameshdlive.xyz":ts.append(tr)
            elif A == "enjoy4hd.site":ts.append(tr)
            elif A == "motornews.live":ts.append(tr)
            elif A == "cr7sports.us":ts.append(tr)
            elif A == "com.methstreams.site":ts.append(tr)
            elif A == "1stream.eu":ts.append(tr)
            elif A == "www.techstips.info":ts.append(tr)
            elif A == "poscitech.com" or "poscitech.org" :ts.append(tr)
            elif A == "en.ripplestream4u.online":ts.append(tr)
            elif A == "rainostreams.com":ts.append(tr)
            elif A == "onionstream.live":ts.append(tr)
            elif A == "livestreames.us":ts.append(tr)
        else:pass
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
        if A == "weakstream.org":from ..extractors.scdn.weakstream import get_link
        elif A == "fabtech.work":from ..extractors.scdn.fabtech import get_link
        elif A == "allsportsdaily.co":from ..extractors.scdn.allsportsdaily import get_link
        elif A == "techclips.net":from ..extractors.scdn.techclips import get_link
        elif A == "gameshdlive.xyz":from ..extractors.scdn.gameshdlive import get_link
        elif A == "enjoy4hd.site":from ..extractors.scdn.enjoy4hd import get_link
        elif A == "motornews.live":from ..extractors.scdn.motornews import get_link
        elif A == "cr7sports.us":from ..extractors.scdn.cr7sports import get_link; A = "nstream.to"
        elif A == "com.methstreams.site":from ..extractors.scdn.methstreams import get_link
        elif A == "1stream.eu":from ..extractors.scdn.onestream import get_link
        elif A == "www.techstips.info":from ..extractors.scdn.techstips import get_link;A = "streamservicehd.click"
        elif A == "poscitech.com" or "poscitech.org":from ..extractors.scdn.poscitech import get_link;A = "streamservicehd.click"
        elif A == "en.ripplestream4u.online":from ..extractors.scdn.ripple import get_link;A = "streamservicehd.click"
        elif A == "rainostreams.com":from ..extractors.scdn.rainostreams import get_link;A = "bdnewszh.com"
        elif A == "onionstream.live":from ..extractors.scdn.onionstream import get_link;A = "wecast.to"
        elif A == "livestreames.us": from ..extractors.scdn.livestreames import get_link; A = "streamservicehd.click"
        m3u8 = get_link(url)
        return m3u8, A


    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url, domain = self.cdn_url(m[self.aid])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name, referrer=f"https://{domain}/")
