from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response
    from ..config import Config
    from ..media import Metadata, Series, Movie

import httpx
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter

from .. import mov_cli_logger

__all__ = ("Scraper",)

class Scraper(ABC): # TODO: Re-add the Configs.
    def __init__(self, config: Config) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        self.__http = httpx.Client(
            timeout = 15.0,
            headers = config.headers,
            cookies = None,
        )

        super().__init__()

    def get(self, url: str, redirect: bool = False) -> Response:
        """Makes a GET request and returns httpx.Response."""
        self.logger.debug(f"GET >> {url}")
        self.__http.headers["Referer"] = url
        return self.__http.get(url, follow_redirects = redirect)

    def post(self, url: str, data: dict = None, json: dict = None) -> Response:
        """Makes a POST request and returns httpx.Response."""
        self.logger.debug(f"POST >> {url}")
        self.__http.headers["Referer"] = url
        return self.__http.post(url, data = data, json = json)

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
        return BeautifulSoup(html, self.config.parser)

    @abstractmethod
    def search(self, query: str) -> Metadata:
        """Where your searching should be done. This will be called upon search operation."""
        ...

    @abstractmethod
    def scrape(self, metadata: Metadata, season: int = None, episode: int = None) -> Series | Movie:
        """Where your scraping for the media should be done. Should return an instance of Media."""
        ...

    def __movie(self) -> dict:
        """When a movie is selected, this will process it. Returns dict"""
        ...

    def __tv(self, season: int, episode: int) -> dict:
        """When a show is selected, this will process it. Returns dict"""
        ...