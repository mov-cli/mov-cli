from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from ..media import Media

import subprocess
from abc import ABC, abstractmethod

__all__ = ("Player",)

class Player(ABC):
    """A base class for all players in mov-cli."""
    def __init__(self, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def play(self, media: Media) -> Optional[subprocess.Popen]:
        """Method to be overridden with code to play media in that specific player."""
        ...