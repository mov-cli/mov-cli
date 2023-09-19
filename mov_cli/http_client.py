from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response
    from .config import Config

import httpx
from devgoldyutils import LoggerAdapter, Colours

from . import mov_cli_logger, errors

__all__ = ("HTTPClient",)

class SiteMaybeBlocked(errors.MovCliException):
    """Raises there's a connection error during a get request."""
    def __init__(self, url: str, error: httpx.ConnectError) -> None:
        super().__init__(
            f"A connection error occurred while making a GET request to '{url}'.\n" \
            "There's most likely nothing wrong with mov-cli. Your ISP's DNS could be blocking this site or perhaps the site is down.\n" \
            f"Actual Error >> {error}"
        )

class HTTPClient():
    def __init__(self, config: Config) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        self.__httpx_client = httpx.Client(
            timeout = 15.0,
            headers = config.headers,
            cookies = None,
        )

        super().__init__()

    def get(self, url: str, redirect: bool = False, **kwargs) -> Response:
        """Performs a GET request and returns httpx.Response."""
        self.logger.debug(Colours.GREEN.apply("GET") + f": {url}")

        self.__httpx_client.headers["Referer"] = url

        try:

            req = self.__httpx_client.get(
                url, follow_redirects = redirect, **kwargs
            )

            self.__httpx_client.headers = self.config.headers

            return req

        except httpx.ConnectError as e:
            raise SiteMaybeBlocked(url, e)
    

    # NOTE: Are we even using post requests, like will they be used in the future? ~ Goldy
    def post(self, url: str, data: dict = None, json: dict = None, **kwargs) -> Response: 
        """Performs a POST request and returns httpx.Response."""
        self.logger.debug(Colours.ORANGE.apply("POST") + f": {url}")

        self.__httpx_client.headers["Referer"] = url

        return self.__httpx_client.post(
            url, data = data, json = json, **kwargs
        )

    def set_header(self, header: dict) -> None:
        """
        Able to set custom headers

        Not recommended
        """
        self.__httpx_client.headers = header

    def add_header_elem(self, header_elem: dict) -> None:
        """Add header elements to default header."""
        for elem in header_elem:
            self.__httpx_client.headers[elem[0]] = elem[1]

    def set_cookies(self, cookies: dict) -> None:
        """Sets cookies."""
        self.__httpx_client.cookies = cookies