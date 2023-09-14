from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HTTPClient

from mov_cli.config import Config
from .sflix import Sflix

__all__ = ("SolarMovies",)

class SolarMovies(Sflix):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.base_url = "https://solarmovie.pe"
        super().__init__(config, http_client)