from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Literal, Optional, Iterable
    from .config import Config
    from .http_client import HTTPClient
    from .media import Metadata, Series, Movie
    from .utils import EpisodeSelector

from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter
from deprecation import deprecated

from . import mov_cli_logger, errors

__all__ = ("Scraper", "MediaNotFound")

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
    def search(self, query: str, limit: int = 20) -> Iterable[Metadata]:
        ...

    @abstractmethod
    def scrape(self, metadata: Metadata, episode: Optional[EpisodeSelector] = None, **kwargs) -> Series | Movie:
        """
        Where your searching and scraping for the media should be performed done. 
        Should return an instance of Media.
        """
        ...

    # TODO: When 'scrape_metadata_episodes' is removed make this an abstract method.
    def scrape_episodes(self, metadata: Metadata, **kwargs) -> Dict[int, int] | Dict[None, Literal[1]]:
        """Returns episode count for each season in that Movie/Series."""
        return self.scrape_metadata_episodes(metadata, **kwargs)

    # NOTE: This won't raise a warning exception as this method is an abstract method but *I think* it will warn on type checkers.
    @deprecated(
        deprecated_in = "4.1.2", 
        removed_in = "4.2.0", 
        details = "'Scraper.scraper_episodes()' should be used instead as we are now removing 'Scraper.scrape_metadata_episodes()'."
    )
    def scrape_metadata_episodes(self, metadata: Metadata, **kwargs) -> Dict[int, int] | Dict[None, Literal[1]]:
        """DEPRECATED! Use 'scrape_episodes' instead, THIS WILL BE REMOVED IN v4.2.0!"""
        ...


class MediaNotFound(errors.MovCliException):
    """Raises when a scraper fails to find a show/movie/tv-station."""
    def __init__(self, message, scraper: Scraper) -> None:
        super().__init__(
            f"Failed to find media: {message}",
            logger = scraper.logger
        )