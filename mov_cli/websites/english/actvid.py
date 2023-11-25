import re
import sys
import base64
import hashlib

# import chardet
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
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
        r = self.client.get(
            f"{self.base_url}/ajax/season/list/{series_id}"
        )  # self.ajax_season
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        z = f"{self.base_url}/ajax/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(z)
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".nav-item > a")]
        ep = self.askepisode(len(episodes))
        episode = episodes[int(ep) - 1]
        return episode, season, ep
    
    def cdn_url(self, final_link: str, rabb_id: str) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(f"{final_link}getSources?id={rabb_id}").json()
        n = self.decryption(data["sources"])
        return n[0]["file"]

    def server_id(self, mov_id: str) -> str:
        req = self.client.get(f"{self.base_url}/ajax/episode/list/{mov_id}")
        soup = BS(req, self.scraper)
        return [i["data-linkid"] for i in soup.select(".nav-item > a")][0]

    def ep_server_id(self, ep_id: str) -> str:
        req = self.client.get(f"{self.base_url}/ajax/episode/servers/{ep_id}")
        soup = BS(req, self.scraper)
        return [i["data-id"] for i in soup.select(".nav-item > a")][0]

    def get_link(self, thing_id: str) -> tuple:
        req = self.client.get(
            f"{self.base_url}/ajax/episode/sources/{thing_id}"
        ).json()["link"]
        print(req)
        return req, self.rabbit_id(req)

    def rabbit_id(self, url: str) -> tuple:
        parts = p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")
        return (
            re.findall(r"(https:\/\/.*\/embed-1)", url)[0].replace(
                "embed-1", "embed-1/ajax/e-1/"
            ),
            parts[-1],
        )

    ## Decrypting the sources

    def gh_key(self):
        response_key = self.client.get('https://github.com/theonlymo/keys/blob/e6/key').json()
        key = response_key["payload"]["blob"]["rawLines"][0]
        key = json.loads(key)
        return key

    def key_extraction(self, string, table):
        sources_array = list(string)

        extracted_key = ""
        current_index = 0

        for index in table:
            start = index[0] + current_index
            end = start + index[1]

            for i in range(start, end):
                extracted_key += sources_array[i]
                sources_array[i] = ' '

            current_index += index[1]

        return extracted_key, ''.join(sources_array)

    def md5(self, input_bytes):
        return hashlib.md5(input_bytes).digest()

    def gen_key(self, salt, secret):
        key = self.md5(secret + salt)
        current_key = key
        while len(current_key) < 48:
            key = self.md5(key + secret + salt)
            current_key += key
        return current_key

    def aes_decrypt(self, decryption_key, source_url):
        cipher_data = self.base64_decode_array(source_url)
        encrypted = cipher_data[16:]
        AES_CBC = AES.new(
            decryption_key[:32], AES.MODE_CBC, iv=decryption_key[32:]
        )
        decrypted_data = unpad(
            AES_CBC.decrypt(encrypted), AES.block_size
        )
        return decrypted_data.decode("utf-8")

    def base64_decode_array(self, encoded_str):
        return bytearray(base64.b64decode(encoded_str))

    def decryption(self, string):
        key, new_string = self.key_extraction(string, self.gh_key())
        decryption_key = self.gen_key(
            self.base64_decode_array(new_string)[8:16], key.encode("utf-8")
        )
        main_decryption = self.aes_decrypt(decryption_key, new_string)
        return json.loads(main_decryption)

    ## End of decrypting the sources

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