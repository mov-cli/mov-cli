from mov_cli.config import Config
from .sflix import Sflix

__all__ = ("SolarMovies",)

class SolarMovies(Sflix):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://solarmovie.pe"
        self._data_linkid = "data-linkid"
        self._select_ = ".nav-item > a"
        super().__init__(config)