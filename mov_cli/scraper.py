from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config
    from .http_client import HTTPClient
    from .media import Metadata, Series, Movie, LiveTV

from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter

from . import mov_cli_logger

__all__ = ("Scraper",)

class Scraper(ABC):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.http_client = http_client
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        super().__init__()

    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, self.config.parser)

    @abstractmethod
    def search(self, query: str) -> Metadata:
        """Where your searching should be done. This will be called upon search operation."""
        ...

    @abstractmethod
    def scrape(self, metadata: Metadata, season: int = None, episode: int = None) -> Series | Movie | LiveTV:
        """Where your scraping for the media should be done. Should return an instance of Media."""
        ...

    def __movie(self) -> dict:
        """When a movie is selected, this will process it. Returns dict"""
        ...

    def __tv(self, season: int, episode: int) -> dict:
        """When a show is selected, this will process it. Returns dict"""
        ...