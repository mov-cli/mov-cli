from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import Tag
    from ..config import Config
    from typing import List, Dict
    from ..http_client import HTTPClient

import re
import json
import base64
import hashlib
from urllib import parse as p
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from .. import utils
from ..utils.scraper import iso_639
from ..media import Series, Movie, Metadata, MetadataType
from ..scraper import Scraper, MediaNotFound

__all__ = ("Sflix",)

class Sflix(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://sflix.se"

        super().__init__(config, http_client)

    def scrape(self, metadata: Metadata, episode: utils.EpisodeSelector = None) -> Series | Movie:
        id = metadata.id

        if episode is None:
            episode = utils.EpisodeSelector()

        if metadata.type == MetadataType.SERIES:
            season_id = self.__get_season_id(episode.season, id)
            epi_id = self.__get_epi_id(season_id, episode.episode)
            sid = self.__ep_server_id(epi_id)
            iframe_url = self.__get_link(sid)
            iframe_link, iframe_id = self.__rabbit_id(iframe_url)
            url, subtitles = self.__cdn(iframe_link, iframe_id)

            return Series(
                url = url,
                title = metadata.title,
                referrer = self.base_url,
                episode = episode,
                season = episode.season,
                subtitles = subtitles
            )

        else:
            sid = self.__server_id(id)
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

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        seasons = None

        if metadata.type == MetadataType.SERIES:
            seasons = {}
            r = self.http_client.get(f"{self.base_url}/ajax/season/list/{metadata.id}").text

            season_ids = [
                i["data-id"] for i in self.soup(r).select(".dropdown-item")
            ]

            for i in range(len(season_ids)):
                rf = self.http_client.get(
                    f"{self.base_url}/ajax/season/episodes/{season_ids[i]}"
                )
                episodes = [i["data-id"] for i in self.soup(rf).select(".episode-item")]
                if len(episodes) >= 1:
                    seasons[i + 1] = len(episodes)
        else:
            return {None: 1}

    def __parse(self, q: str) -> str:
        return q.replace(" ", "-").lower()

    def search(self, query: str, limit: int = None) -> List[Metadata]:
        response = self.http_client.get(
            f"{self.base_url}/search/{p.quote(self.__parse(query))}"
        )
        soup = self.soup(response)

        results = []
        items: List[Tag] = soup.findAll("div", {"class": "flw-item"}, limit = limit)

        for item in items:
            fdi_items = item.findAll("span", {"class": "fdi-item"})
            item_url = item.select(".film-poster-ahref")[0]["href"]
            item_type = fdi_items[1].text

            results.append(
                Metadata(
                    id = item_url.split("-")[-1],
                    title = item.select(".film-name > a")[0].text,
                    type = MetadataType.MOVIE if item_type.lower() == "movie" else MetadataType.SERIES, 
                    year = fdi_items[0].text
                )
            )

        return results

    def __cdn(self, final_link: str, rabb_id: str) -> str:
        subtitles = {}
        data = self.http_client.get(f"{final_link}getSources?id={rabb_id}", headers = {"X-Requested-With": "XMLHttpRequest"}).json()
        for item in data["tracks"]:
            item : dict
            file = item.get("file")
            label = item.get("label")
            prefix = iso_639.get(label, None)
            if label.__contains__("-") or label.__contains__(" "):
                continue

            subtitles[prefix] = {}
            subtitles[prefix]["label"] = label
            subtitles[prefix]["file"] = file
        
        n = self.__decryption(data["sources"])
        return n[0]["file"], subtitles

    def __server_id(self, mov_id):
        rem = self.http_client.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = self.soup(rem)
        server_ids = [i["data-id"] for i in soup.select(".link-item")]

        if len(server_ids) == 0:
            raise MediaNotFound("No server id's were retrieved so we can't scrape for your media.", self)

        return server_ids[0]

    def __ep_server_id(self, ep_id):
        rem = self.http_client.get(
            f"{self.base_url}/ajax/episode/servers/{ep_id}"
        )
        soup = self.soup(rem)
        return [i["data-id"] for i in soup.select(".link-item")][0]

    def __get_epi_id(self, season_id: str, episode: int) -> str:
        r = self.http_client.get(
            f"{self.base_url}/ajax/season/episodes/{season_id}"
        )
        episodes = [i["data-id"] for i in self.soup(r).select(".episode-item")]
        episode = episodes[episode - 1]
        return episode

    def __get_link(self, thing_id: str) -> tuple:
        req = self.http_client.get(f"{self.base_url}/ajax/sources/{thing_id}").json()["link"]
        return req

    def __rabbit_id(self, url: str) -> tuple:
        parts = p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")
        return (
            re.findall(r"(https:\/\/.*\/embed-4)", url)[0].replace(
                "embed-4", "ajax/embed-4/"
            ),
            parts[-1],
        )

    def __get_season_id(self, season: int, id : str) -> str:
        r = self.http_client.get(f"{self.base_url}/ajax/season/list/{id}").text

        season_ids = [
            i["data-id"] for i in self.soup(r).select(".dropdown-item")
        ]
        return season_ids[season - 1]

    def __gh_key(self):
        response_key = self.http_client.get(
            "https://github.com/theonlymo/keys/blob/e4/key", 
            headers = {"X-Requested-With": "XMLHttpRequest"},
            include_default_headers = False
        ).json()
        key = response_key["payload"]["blob"]["rawLines"][0]
        key = json.loads(key)
        return key

    def __key_extraction(self, string, table):
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