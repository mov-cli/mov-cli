from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..media import Media
    from typing import Literal
    from httpx import Response
    from ..config import Config

import json
import httpx
from abc import ABC
from bs4 import BeautifulSoup
from importlib.util import find_spec
from devgoldyutils import LoggerAdapter

from .. import mov_cli_logger

__all__ = ("Scraper",)

DEFAULT_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

class Scraper(ABC): # TODO: Re-add the Configs.
    def __init__(self) -> None:
        """A base class for building scrapers from."""
        self.__http = httpx.Client(
            timeout = 15.0,
            headers = DEFAULT_HEADERS,
            cookies = None,
        )

        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        super().__init__()

    @property
    def parser(self) -> Literal["lxml", "html.parser"]:
        if find_spec("lxml"):
            return "lxml"

        return "html.parser"

    def get(self, url: str, redirect: bool = False) -> Response:
        """Makes a GET request and returns httpx.Response"""
        self.logger.debug(f"GET: {url}")

        self.__http.headers["Referer"] = url

        get = self.__http.get(url, follow_redirects=redirect)

        return get

    def post(self, url: str, data: dict = None, json: dict = None) -> Response:
        """Makes a POST request and returns httpx.Response"""
        self.logger.debug(f"POST: {url}")

        self.__http.headers["Referer"] = url

        post = self.__http.post(url, data=data, json=json)

        return post

    def set_header(self, header: dict) -> None:
        """
        Able to set custom headers

        Not recommended
        """
        self.__http.headers = header

    def add_header_elem(self, header_elem: dict) -> None:
        """Add header elements to default header."""
        for elem in header_elem:
            self.__http.headers[elem[0]] = elem[1]

    def set_cookies(self, cookies: dict) -> None:
        """Sets cookies."""
        self.__http.cookies = cookies

    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, self.parser)        

    def make_json(
        self,
        title: str,
        url: str,
        type: Literal["show", "movie"],
        referrer: str,
        img: str = None,
        seasons: int = None,
        season: int = None,
        episode: int = None,
        year: str = None,
    ) -> dict:
        js = json.loads("{}")
        js["title"] = title
        js["url"] = url
        js["type"] = type
        js["referrer"] = referrer
        js["img"] = img
        js["seasons"] = seasons
        js["season"] = season
        js["episode"] = episode
        js["year"] = year
        return js

    def search(self, query: str) -> dict:
        """Search anything. Returns dict"""
        ...

    def __results(self, response: Response) -> dict:
        """Processes Search. Returns dict"""
        ...

    def select(self, selection: int) -> None:
        """Select a dict. Returns None"""

    def get_seasons(self) -> int:
        """Get Season. Returns int"""
        ...

    def get_episodes(self, season: int) -> int:
        """Get Episodes. Return int"""
        ...

    def get_media(self, season: int = None, episode: int = None) -> Media:
        """Gets Media. Returns Media Object."""
        ...

    def __movie(self) -> dict:
        """When a movie is selected, this will process it. Returns dict"""
        ...

    def __tv(self, season: int, episode: int) -> dict:
        """When a show is selected, this will process it. Returns dict"""
        ...