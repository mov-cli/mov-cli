from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config

from .sflix import Sflix

__all__ = ("DopeBox",)

class DopeBox(Sflix):
    def __init__(self, config: Config) -> None:
        self.base_url = "https://dopebox.to"
        super().__init__(config)