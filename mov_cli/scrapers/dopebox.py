from mov_cli.config import Config
from .sflix import Sflix

class DopeBox(Sflix):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://dopebox.to"
        super().__init__(config)