from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from .config import Config

import requests

from .utils import EpisodeSelector
from .errors import SubtitlesKeyMissing

__all__ = (
    "Subtitles",
)

class Subtitles:
    """
    pull subtitles from api.opensubtitles.com and return
    a link to the .srt file which can be passed into vlc or mpv
    """
    def __init__(self, config: Config, language: str = "en"):
        self.language = language
        self.key = config.open_subtitles_key

        if self.key is None:
            raise SubtitlesKeyMissing("open subtitles")

        self.base_url = "https://api.opensubtitles.com/api/v1"

        self.get_headers = {
            "User-Agent": "mov-cli",
            "Api-Key": self.key,
        }

    def get_subtitles(self, name: str, episode: Optional[EpisodeSelector]) -> str:
        params = {
            "query": name,
            "languages": self.language
        }

        if episode is not None:
            params["episode_number"] = episode.episode
            params["season_number"] = episode.season

        response = requests.get(
            self.base_url + "/subtitles/", 
            params = params,
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