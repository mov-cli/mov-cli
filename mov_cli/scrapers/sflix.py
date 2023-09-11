from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from httpx import Response
    from ..config import Config
    from bs4 import BeautifulSoup

import re

from .. import scraper_utils
from ..scraper import Scraper
from ..media import Series, Movie

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib import parse as p
from ..media import Metadata, MetadataType
import hashlib
import json
import base64
from devgoldyutils import pprint

__all__ = ("Sflix",)

class Sflix(Scraper):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://sflix.se"
        self.season_ids = {}

        self._data_linkid = "data-id"
        self._select_ = ".dropdown-item"

        super().__init__(config)


    def __parse(self, q: str) -> str:
        return q.replace(" ", "-").lower()


    def search(self, q: str) -> List[Metadata]:
        search_req = self.get(f"{self.base_url}/search/{self.__parse(q)}")
        results = self.__results(search_req)
        return results

    def __results(self, html: Response) -> List[Metadata]:
        soup = self.soup(html)
        items = soup.findAll("div", {"class": "flw-item"})
        metadata_list = []
        for item in items:
            item: BeautifulSoup
            url = item.select(".film-poster-ahref")[0]["href"]
            
            type = None
            if url.__contains__("/movie/"):
                type = MetadataType.MOVIE
            else:
                type = MetadataType.SERIES
            
            title = item.select(".film-name > a")[0].text
            
            id = url.split("-")[-1]

            year = item.find("span", {"class": "fdi-item"}).text

            img = item.select(".film-poster-img")[0]["data-src"]

            seasons = None # 

            if type == MetadataType.SERIES:
                print(MetadataType.SERIES)
                seasons = {}
                r = self.get(f"{self.base_url}/ajax/season/list/{id}").text

                self.season_ids = [
                    i[self._data_linkid] for i in self.soup(r).select(self._select_)
                ]
                print(self.season_ids)

                for i in range(len(self.season_ids)):
                    rf = self.get(
                        f"{self.base_url}/ajax/season/episodes/{self.season_ids[i]}"
                    )
                    episodes = [i[self._data_linkid] for i in self.soup(rf).select(".episode-item")]
                    print(episodes)
                    if len(episodes) >= 1:
                        seasons[i + 1] = len(episodes)
                    
            if seasons is not None and len(seasons) == 0:
                print(seasons, len(seasons))
                continue

            metadata_list.append(
                Metadata(
                    id = id,
                    title = title,
                    type = type,
                    image_url= img,
                    seasons = seasons,
                    year = year
                )
            )
        return metadata_list
    

    def __cdn(self, final_link: str, rabb_id: str) -> str:
        subtitles = json.loads("{}")
        self.set_header({"X-Requested-With": "XMLHttpRequest"})
        data = self.get(f"{final_link}getSources?id={rabb_id}").json()
        for item in data["tracks"]:
            item : dict
            file = item.get("file")
            label = item.get("label")
            prefix = scraper_utils.get_prefix(label)
            if label.__contains__("-") or label.__contains__(" "):
                continue

            subtitles[prefix] = {}
            subtitles[prefix]["label"] = label
            subtitles[prefix]["file"] = file
        
        n = self.__decryption(data["sources"])
        pprint(subtitles)
        return n[0]["file"], subtitles

    def __server_id(self, mov_id):
        rem = self.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = self.soup(rem)
        return [i[self._data_linkid] for i in soup.select(".link-item")][0]

    def __ep_server_id(self, ep_id):
        rem = self.get(
            f"{self.base_url}/ajax/episode/servers/{ep_id}"
        )
        soup = self.soup(rem)
        return [i[self._data_linkid] for i in soup.select(".link-item")][0]

    def __get_epi_id(self, season_id: str, episode: int) -> str:
        r = self.get(
            f"{self.base_url}/ajax/season/episodes/{season_id}"
        )
        episodes = [i[self._data_linkid] for i in self.soup(r).select(".episode-item")]
        episode = episodes[episode - 1]
        return episode


    def __get_link(self, thing_id: str) -> tuple:
        req = self.get(f"{self.base_url}/ajax/sources/{thing_id}").json()["link"]
        print(req)
        return req

    def __rabbit_id(self, url: str) -> tuple:
        parts = p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")
        return (
            re.findall(r"(https:\/\/.*\/embed-4)", url)[0].replace(
                "embed-4", "ajax/embed-4/"
            ),
            parts[-1],
        )


    def __gh_key(self):
        response_key = self.get('https://github.com/enimax-anime/key/blob/e4/key.txt').json()
        key = response_key["payload"]["blob"]["rawLines"][0]
        key = json.loads(key)
        return key

    def __key_extraction(self, string, table):
        decrypted_key = []
        offset = 0
        encrypted_string = string

        for start, end in table:
            decrypted_key.append(encrypted_string[start - offset:end - offset])
            encrypted_string = (
                encrypted_string[:start - offset] + encrypted_string[end - offset:]
            )
            offset += end - start

        return "".join(decrypted_key), encrypted_string

    def __md5(self, input_bytes):
        return hashlib.md5(input_bytes).digest()

    def __gen_key(self, salt, secret):
        key = self.__md5(secret + salt)
        current_key = key
        while len(current_key) < 48:
            key = self.__md5(key + secret + salt)
            current_key += key
        return current_key

    def __aes_decrypt(self, decryption_key, source_url):
        cipher_data = self.__base64_decode_array(source_url)
        encrypted = cipher_data[16:]
        AES_CBC = AES.new(
            decryption_key[:32], AES.MODE_CBC, iv=decryption_key[32:]
        )
        decrypted_data = unpad(
            AES_CBC.decrypt(encrypted), AES.block_size
        )
        return decrypted_data.decode("utf-8")

    def __base64_decode_array(self, encoded_str):
        return bytearray(base64.b64decode(encoded_str))

    def __decryption(self, string):
        key, new_string = self.__key_extraction(string, self.__gh_key())
        decryption_key = self.__gen_key(
            self.__base64_decode_array(new_string)[8:16], key.encode("utf-8")
        )
        main_decryption = self.__aes_decrypt(decryption_key, new_string)
        return json.loads(main_decryption)
    
    def scrape(self, metadata: Metadata, episode: int = None, season: int = None) -> Series | Movie:
        if metadata.type == MetadataType.SERIES:
            season_id = self.season_ids[season - 1]
            epi_id = self.__get_epi_id(season_id, episode)
            sid = self.__ep_server_id(epi_id)
            iframe_url = self.__get_link(sid)
            iframe_link, iframe_id = self.__rabbit_id(iframe_url)
            url, subtitles = self.__cdn(iframe_link, iframe_id)
            
            return Series(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                episode = episode,
                season = season,
                subtitles = subtitles
            )
        else:
            sid = self.__server_id(metadata.id)
            iframe_url = self.__get_link(sid)
            iframe_link, iframe_id = self.__rabbit_id(iframe_url)
            url, subtitles = self.__cdn(iframe_link, iframe_id)
            
            return Movie(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                year = metadata.year,
                subtitles = subtitles
            )

