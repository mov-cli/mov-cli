import httpx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response
    from ..config import Config
    from ..media import Media

from devgoldyutils import LoggerAdapter

from .. import mov_cli_logger


DEFAULT_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

__all__ = ("Scraper",)

class Scraper():
    def __init__(self, base_url: str, config: Config) -> None:
        """Anything HTTP/HTTPS related for mov-cli"""   
        self.config = config
        
        self.__http = httpx.Client(timeout=15.0, headers=DEFAULT_HEADERS, cookies=None, proxies=self.config.proxy)

        self.base_url = base_url

        self.logger = LoggerAdapter(mov_cli_logger, prefix = "Scraper")

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

    def search(self, query: str) -> dict:
        """Search anything. Returns dict"""
        ...

    def __results(self, response: Response) -> dict:
        """Processes Search. Returns dict"""
        ...

    def select(self, selection: int) -> None:
        """Select a dict. Returns None"""

    def getSeasons(self) -> int:
        """Get Season. Returns int"""
        ...

    def getEpisodes(self, season: int) -> int:
        """Get Episodes. Return int"""
        ...
    
    def getMedia(self, season: int = None, episode: int = None) -> Media: # TODO: Find better name
        """Get URL. Returns Media Object."""
        ...

    def __movie(self) -> dict:
        """When a movie is selected, this will process it. Returns dict"""
        ...

    def __tv(self, season: int, episode: int) -> dict:
        """When a show is selected, this will process it. Returns dict"""
        ...