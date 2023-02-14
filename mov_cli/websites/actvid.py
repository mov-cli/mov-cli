import re
import sys
import base64
import hashlib
# import chardet
from Crypto.Cipher import AES
from typing import Callable, Any
from urllib import parse as p
from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import json

sys.path.append("..")

x: Callable[[Any], str] = (
    lambda d: base64.b64encode(d.encode()).decode().replace("\n", "").replace("=", ".")
)


class Actvid(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.userinput = None
        self.base_url = base_url
        self.rep_key = (
            "6LfV6aAaAAAAAC-irCKNuIS5Nf5ocl5r0K3Q0cdz"  # Google Recaptcha key
        )
        self.rab_domain = x(
            "https://rabbitstream.net:443"
        )
        # encoding and then decoding the url
        # self.redo()
        # IMP: self.client.get/post always returns a response object
        # self.client.post/get -> httpx.response

    """def key_num(self, iframe_link: str) -> tuple:
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
        )"""

    def search(self, q: str = None) -> str:
        q = (
            input("[!] Please Enter the name of the Movie: ")
            if q is None
            else q
        )
        self.userinput = q
        return self.client.get(f"{self.base_url}/search/{self.parse(q)}").text

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

    def ask(self, series_id: str) -> tuple:
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "lxml").select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, "lxml").select(".nav-item > a")]
        episode = episodes[
            int(self.askepisode(len(episodes))) - 1
            ]
        ep = self.getep(url=f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}",
                        data_id=f"{episode}")
        return episode, season, ep

    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text

        soup = BS(source, "lxml")

        unformated = soup.find("a", {"data-id": f"{data_id}"})['title']

        formated = unformated.split("Eps")[1]
        formated = formated.split(":")[0]

        return formated

    """    def websocket(self, iframe_id):
        # Thanks to Twilight for fixing it.
        '''
        will return decryption key, sources and tracks
        '''
        ws = create_connection("wss://wsx.dokicloud.one/socket.io/?EIO=4&transport=websocket")
        p = ws.recv()
        code = re.findall(self.CODE_REGEX, p)[0]

        # dirty impleamentation
        if code == "0":
            ws.send("40")
            p = ws.recv()

            code = re.findall(self.CODE_REGEX, p)[0]

            if code == "40":
                key = re.findall(self.SID_REGEX, p)[0]

                ws.send(
                    '42["getSources",{"id":"' + iframe_id + '"}]'
                )
                p = ws.recv()
                x = json.loads(re.findall(self.SOURCE_REGEX, p)[0])

        return key, x["sources"], x["tracks"]

    def cdn_url(self, rabb_id: str) -> str:
        key, source, track = self.websocket(rabb_id)
        predata = self.decrypt(source, bytes(key, "utf-8"))
        data = json.loads(predata)
        print(predata)
        return data[0]['file']"""

    def cdn_url(self, final_link: str, rabb_id: str) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(
            f"{final_link}getSources?id={rabb_id}"
        ).json()
        source = data['sources']
        link = f"{source}"
        if link.endswith("==") or link.endswith("="):
            n = json.loads(self.decrypt(data['sources'], self.gh_key()))
            return n[0]['file']
        return source[0]['file']

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

    def rabbit_id(self, url: str) -> tuple:
        parts = p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")
        return re.findall(r'(https:\/\/.*\/embed-4)', url)[0].replace("embed-4", "ajax/embed-4/"), parts[-1]

    ## decryption
    ## Thanks to Twilight

    # def determine_char_enc(self, value):
    #    result = chardet.detect(value)['encoding']
    #    return result

    # websocket simulation

    def gh_key(self):
        u = self.client.get("https://raw.githubusercontent.com/mov-cli/movkey/main/key.txt").text
        return bytes(u, 'utf-8')


    def md5(self, data):
        return hashlib.md5(data).digest()

    def get_key(self, salt, key):
        x = self.md5(key + salt)
        currentkey = x
        while (len(currentkey) < 48):
            x = self.md5(x + key + salt)
            currentkey += x
        return currentkey

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, data, key):
        k = self.get_key(
            base64.b64decode(data)[8:16], key
        )
        dec_key = k[:32]
        iv = k[32:]
        p = AES.new(dec_key, AES.MODE_CBC, iv=iv).decrypt(
            base64.b64decode(data)[16:]
        )
        return self.unpad(p).decode()
    
    def ds(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "lxml").select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, "lxml").select(".nav-item > a")]
        for e in range(len(episodes)):
            episode = episodes[e]
            sid = self.ep_server_id(episode)
            iframe_url, tv_id = self.get_link(sid)
            iframe_link, iframe_id = self.rabbit_id(iframe_url)
            url = self.cdn_url(iframe_link, iframe_id)
            self.dl(url, name, season=season, episode=e+1)

    def sd(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "lxml").select(".dropdown-item")
        ]
        for s in range(len(season_ids)):
            z = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[s]}"
            rf = self.client.get(z)
            episodes = [i["data-id"] for i in BS(rf, "lxml").select(".nav-item > a")]
            for e in range(len(episodes)):
                episode = episodes[e]
                sid = self.ep_server_id(episode)
                iframe_url, tv_id = self.get_link(sid)
                iframe_link, iframe_id = self.rabbit_id(iframe_url)
                url = self.cdn_url(iframe_link, iframe_id)
                self.dl(url, name, season=s+1, episode=e+1)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd" or "ds"):
        name = t[self.title]
        if state == "sd":
            self.sd(t[self.aid],name)
            return
        if state == "ds":
            self.ds(t[self.aid],name)
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
        if state == "sd":
            print("You can download only Shows with 'sd'")
            return
        self.play(url, name)

    def SandR(self, q: str = None):
        return self.results(self.search(q))

    def redo(self, query: str = None, result: int = None):
        return self.display(query)
