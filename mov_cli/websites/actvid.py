import re
import sys
import json
import base64
from typing import Callable, Any
from urllib import parse as p

from ..utils.history import History
from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
from ..utils.presence import update_presence

sys.path.append("..")

x: Callable[[Any], str] = (
    lambda d: base64.b64encode(d.encode()).decode().replace("\n", "").replace("=", ".")
)


class Actvid(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.rep_key = (
            "6LfV6aAaAAAAAC-irCKNuIS5Nf5ocl5r0K3Q0cdz"  # Google Recaptcha key
        )
        self.rab_domain = x(
            "https://rabbitstream.net:443"
        )  # encoding and then decoding the url
        # self.redo()
        # IMP: self.client.get/post always returns a response object
        # self.client.post/get -> httpx.response

    def key_num(self, iframe_link: str) -> tuple:
        self.client.add_elem(
            {"Referer": self.base_url}
        )  # adding referer to the headers
        # self.client.headers['Referer'] = self.base_url
        req = self.client.get(iframe_link).text
        soup = BS(req, "lxml")
        k = list([i.text for i in soup.find_all("script")][-3].replace("var", ""))
        key, num = "".join(k[21:61]), k[-3]
        return key, num  # returns a tuple

    def auth_token(self, key: str) -> str:
        self.client.add_elem({"Referer": self.base_url})
        self.client.add_elem({"cacheTime": "0"})  # adding referer to the headers
        r = self.client.get(
            f"https://www.google.com/recaptcha/api.js?render={self.rep_key}"
        )
        s = r.text.replace("/* PLEASE DO NOT COPY AND PASTE THIS CODE. */", "")
        s = s.split(";")
        v_token = s[10].replace("po.src=", "").split("/")[-2]
        r = self.client.get(
            f"https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=xxmovclix&k={key}&co={self.rab_domain}&v={v_token}"
        ).text
        soup = BS(r, "lxml")
        recap_token = [i["value"] for i in soup.select("#recaptcha-token")][0]
        data = {
            "v": v_token,
            "k": self.rep_key,
            "c": recap_token,
            "co": self.rab_domain,
            "sa": "",
            "reason": "q",
        }
        self.client.add_elem({"cacheTime": "0"})
        return json.loads(
            self.client.post(
                f"https://www.google.com/recaptcha/api2/reload?k={key}", data=data
            ).text.replace(")]}'", "")
        )

    def search(self, query: str = None) -> str:
        query = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if query is None
            else query
        )
        self.userinput = query
        return self.client.get(f"{self.base_url}/search/{self.parse(query)}").text

    def results(self, html: str) -> list:
        soup = BS(html, "lxml")
        urls = [i["href"] for i in soup.select(".film-poster-ahref")]
        mov_or_tv = [
            "MOVIE" if i["href"].__contains__("/movie/") else "TV"
            for i in soup.select(".film-poster-ahref")
        ]
        title = [
            re.sub(
                pattern="full|/tv/|/movie/|hd|watch|[0-9]{2,}",
                repl="",
                string=" ".join(i.split("-")),
            )
            for i in urls
        ]
        ids = [i.split("-")[-1] for i in urls]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, series_id: str) -> str:
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "lxml").select(".dropdown-item")
        ]
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{len(season_ids)}): "
            )
        )
        z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, "lxml").select(".nav-item > a")]
        episode = episodes[
            int(
                input(
                    self.lmagenta(
                        f"Please input the episode number(total episodes in season:{season}):{len(episodes)} : "
                    )
                )
            )
            - 1
        ]
        ep = self.getep(url=f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}", data_id=f"{episode}")
        return episode, season, ep


    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text

        soup = BS(source, "lxml")

        unformated = soup.find("a", {"data-id": f"{data_id}"})['title']

        formated = unformated.split("Eps")[1]
        formated = formated.split(":")[0]

        return formated

    def cdn_url(self, rabb_id: str, rose: str, num: str) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(
            f"https://mzzcloud.life/ajax/embed-4/getSources?id={rabb_id}&_token={rose}&_number={num}"
        ).json()["sources"][0]["file"]
        return data

    def server_id(self, mov_id: str) -> str:
        req = self.client.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = BS(req, "lxml")
        return [i["data-linkid"] for i in soup.select(".nav-item > a")][0]

    def ep_server_id(self, ep_id: str) -> str:
        req = self.client.get(
            f"{self.base_url}/ajax/v2/episode/servers/{ep_id}/#servers-list"
        )
        soup = BS(req, "lxml")
        return [i["data-id"] for i in soup.select(".nav-item > a")][0]

    def get_link(self, thing_id: str) -> tuple:
        req = self.client.get(f"{self.base_url}/ajax/get_link/{thing_id}").json()[
            "link"
        ]
        print(req)
        return req, self.rabbit_id(req)

    def rabbit_id(self, url: str) -> str:
        return p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")[-1]

    def TV_PandDP(self, t: list, state: str = "d" or "p"):
        name = t[self.title]
        episode, season, ep = self.ask(t[self.aid])
        sid = self.ep_server_id(episode)
        iframe_url, tv_id = self.get_link(sid)
        key, num = self.key_num(iframe_url)
        token = self.auth_token(key)[1]
        url = self.cdn_url(tv_id, token, num)
        History.addhistory(name, state, "")
        if state == "d":
            self.dl(url, name)
            return
        update_presence(self.userinput, season, ep)
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        sid = self.server_id(m[self.aid])
        iframe_url, mov_id = self.get_link(sid)
        key, num = self.key_num(iframe_url)
        token = self.auth_token(key)[1]
        url = self.cdn_url(mov_id, token, num)
        History.addhistory(name, state, "")
        if state == "d":
            self.dl(url, name)
            return
        update_presence(self.userinput)
        self.play(url, name)

    def SandR(self, q: str = None):
        return self.results(self.search(q))

    def redo(self, query: str = None, result: int = None):
        return self.display(query)
