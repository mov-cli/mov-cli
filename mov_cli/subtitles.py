from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .utils.episode_selector import EpisodeSelector

import requests

__all__ = (
    "Subtitles",
)

class Subtitles:
    """
    pull subtitles from api.opensubtitles.com and return
    a link to the .srt file which can be passed into vlc or mpv
    """
    def __init__(self, key: str, language: str = "en"):
        self.language = language
        self.key = key
        self.base_url = "https://api.opensubtitles.com/api/v1"
        self.get_headers = {
            "User-Agent": "mov-cli",
            "Api-Key": f"{key}",
        }

    def get_tv_subs(self, name: str, episode: EpisodeSelector) -> str:
        response = requests.get(
            self.base_url + "/subtitles/", 
            params = {
                "query": name,
                "languages": self.language,
                "episode_number": episode.episode,
                "season_number": episode.season
            },
            headers = self.get_headers
        )

        return self.__get_link(response.json()["data"][0]['attributes']['files'][0]['file_id'])

    def get_movie_subs(self, name: str) -> str:
        response = requests.get(
            self.base_url + "/subtitles/", 
            params = {
                "query": name,
                "languages": self.language
            },
            headers = self.get_headers
        )

        return self.__get_link(response.json()["data"][0]['attributes']['files'][0]['file_id'])

    def __get_link(self, file_id) -> str:
        headers = {
            "User-Agent": "movcli",
            "Api-Key": f"{self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {"file_id": f"{file_id}"}

        response = requests.post(self.base_url + "/download", json = payload, headers = headers)
        return response.json()['link']


subtitles = Subtitles("KEY")
print(subtitles.get_tv_subs("community", 4, 1))
