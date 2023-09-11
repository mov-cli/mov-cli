from mov_cli.config import Config
from .sflix import Sflix

__all__ = ("SolarMovies",)

class SolarMovies(Sflix):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://solarmovie.pe"
        super().__init__(config)