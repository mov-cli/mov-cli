import re
import sys
import base64
import hashlib

# import chardet
from Crypto.Cipher import AES
from urllib import parse as p
from ...utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import json

sys.path.append("..")


def x(d):
    return base64.b64encode(d.encode()).decode().replace("\n", "").replace("=", ".")


class Provider(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.dseasonp = True
        self.dshowp = True

    def search(self, q: str = None) -> str:
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return self.client.get(f"{self.base_url}/search/{self.parse(q)}").text

    def results(self, html: str) -> list:
        soup = BS(html, self.scraper)
        urls = [i["href"] for i in soup.select(".film-poster-ahref")]
        mov_or_tv = [
            "MOVIE" if i["href"].__contains__("/movie/") else "TV"
            for i in soup.select(".film-poster-ahref")
        ]
        title = [i.text for i in soup.select(".film-name > a")]
        ids = [i.split("-")[-1] for i in urls]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, series_id: str) -> tuple:
        r = self.client.get(f"{self.base_url}/ajax/season/list/{series_id}") # self.ajax_season
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        z = f"{self.base_url}/ajax/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".nav-item > a")]
        episode = episodes[int(self.askepisode(len(episodes))) - 1]
        ep = self.getep(
            url=f"{self.base_url}/ajax/season/episodes/{season_ids[int(season) - 1]}",
            data_id=f"{episode}",
        )
        return episode, season, ep

    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text

        soup = BS(source, self.scraper)

        unformated = soup.find("a", {"data-id": f"{data_id}"})["title"]

        formated = unformated.split("Eps")[1]
        formated = formated.split(":")[0]

        return formated

    def cdn_url(self, final_link: str, rabb_id: str) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(f"{final_link}getSources?id={rabb_id}").json()
        n = json.loads(self.decrypt(data["sources"], self.gh_key()))
        return n[0]["file"]

    def server_id(self, mov_id: str) -> str:
        req = self.client.get(f"{self.base_url}/ajax/episode/list/{mov_id}")
        soup = BS(req, self.scraper)
        return [i["data-linkid"] for i in soup.select(".nav-item > a")][0]

    def ep_server_id(self, ep_id: str) -> str:
        req = self.client.get(
            f"{self.base_url}/ajax/episode/servers/{ep_id}"
        )
        soup = BS(req, self.scraper)
        return [i["data-id"] for i in soup.select(".nav-item > a")][0]

    def get_link(self, thing_id: str) -> tuple:
        req = self.client.get(f"{self.base_url}/ajax/episode/sources/{thing_id}").json()[
            "link"
        ]
        print(req)
        return req, self.rabbit_id(req)

    def rabbit_id(self, url: str) -> tuple:
        parts = p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")
        return (
            re.findall(r"(https:\/\/.*\/embed-4)", url)[0].replace(
                "embed-4", "ajax/embed-4/"
            ),
            parts[-1],
        )

    def gh_key(self):
        u = self.client.get(
            "https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt"
        ).text
        return bytes(u, "utf-8")

    def md5(self, data):
        return hashlib.md5(data).digest()

    def get_key(self, salt, key):
        x = self.md5(key + salt)
        currentkey = x
        while len(currentkey) < 48:
            x = self.md5(x + key + salt)
            currentkey += x
        return currentkey

    def unpad(self, s):
        return s[: -ord(s[len(s) - 1 :])]

    def decrypt(self, data, key):
        k = self.get_key(base64.b64decode(data)[8:16], key)
        dec_key = k[:32]
        iv = k[32:]
        p = AES.new(dec_key, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data)[16:])
        return self.unpad(p).decode()   

    def ds(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".nav-item > a")]
        for e in range(len(episodes)):
            episode = episodes[e]
            sid = self.ep_server_id(episode)
            iframe_url, tv_id = self.get_link(sid)
            iframe_link, iframe_id = self.rabbit_id(iframe_url)
            url = self.cdn_url(iframe_link, iframe_id)
            self.dl(url, name, season=season, episode=e + 1)

    def sd(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        for s in range(len(season_ids)):
            z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[s]}"
            rf = self.client.get(z)
            episodes = [
                i["data-id"] for i in BS(rf, self.scraper).select(".nav-item > a")
            ]
            for e in range(len(episodes)):
                episode = episodes[e]
                sid = self.ep_server_id(episode)
                iframe_url, tv_id = self.get_link(sid)
                iframe_link, iframe_id = self.rabbit_id(iframe_url)
                url = self.cdn_url(iframe_link, iframe_id)
                self.dl(url, name, season=s + 1, episode=e + 1)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd" or "ds"):
        name = t[self.title]
        if state == "s":
            self.sd(t[self.aid], name)
            return
        if state == "e":
            self.ds(t[self.aid], name)
            return
        episode, season, ep = self.ask(t[self.aid])
        sid = self.ep_server_id(episode)
        iframe_url, tv_id = self.get_link(sid)
        iframe_link, iframe_id = self.rabbit_id(iframe_url)
        url = self.cdn_url(iframe_link, iframe_id)
        if state == "d":
            self.dl(url, name, season=season, episode=ep)
            return
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        sid = self.server_id(m[self.aid])
        iframe_url, tv_id = self.get_link(sid)
        iframe_link, iframe_id = self.rabbit_id(iframe_url)
        url = self.cdn_url(iframe_link, iframe_id)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)

    def SandR(self, q: str = None):
        return self.results(self.search(q))

    def redo(self, query: str = None, result: int = None):
        return self.display(query)
