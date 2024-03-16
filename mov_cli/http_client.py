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
            "There's most likely nothing wrong with mov-cli. Your ISP's DNS could be blocking this site or perhaps the site is down. " \
            f"{Colours.GREEN}SOLUTION: Use a VPN or switch DNS!{Colours.RED}\n" \
            f"Actual Error >> {error}"
        )

class HTTPClient():
    def __init__(self, config: Config) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        self.__httpx_client = httpx.Client(
            timeout = 15.0,
            cookies = None
        )

        super().__init__()

    def get(
        self, 
        url: str, 
        headers: dict = {}, 
        include_default_headers: bool = True, 
        redirect: bool = False, 
        **kwargs
    ) -> Response:
        """Performs a GET request and returns httpx.Response."""
        self.logger.debug(Colours.GREEN.apply("GET") + f" -> {url}")

        if include_default_headers is True:
            headers.update({"Referer": url})
            headers.update(self.config.http_headers)

        try:
            response = self.__httpx_client.get(
                url, 
                headers = headers, 
                follow_redirects = redirect, 
                **kwargs
            )

            if response.is_error:
                self.logger.error(
                    f"GET Request to {response.url} failed! ({response})"
                )

            return response

        except httpx.ConnectError as e:
            if "[SSL: CERTIFICATE_VERIFY_FAILED]" in str(e):
                raise SiteMaybeBlocked(url, e)

            raise e

    def post(self, url: str, data: dict = None, json: dict = None, **kwargs) -> Response: 
        """Performs a POST request and returns httpx.Response."""
        self.logger.debug(Colours.ORANGE.apply("POST") + f": {url}")

        self.__httpx_client.headers["Referer"] = url

        return self.__httpx_client.post(
            url, data = data, json = json, **kwargs
        )

    def set_cookies(self, cookies: dict) -> None:
        """Sets cookies."""
        self.__httpx_client.cookies = cookies