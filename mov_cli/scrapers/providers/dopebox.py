from mov_cli.config import Config
from .sflix import Sflix

class DopeBox(Sflix):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.base_url = "https://dopebox.to"