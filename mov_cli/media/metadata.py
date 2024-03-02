from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Callable, Optional

from enum import Enum
from dataclasses import dataclass, field

__all__ = ("MetadataType", "Metadata", "ExtraMetadata", "AiringType")

class MetadataType(Enum):
    SERIES = 0
    MOVIE = 1
    LIVE_TV = 2

class AiringType(Enum):
    DONE = 0
    ONGOING = 1
    PRODUCTION = 2
    RELEASED = 3
    CANCELED = 4

@dataclass
class Metadata:
    """Search results from the providers."""
    id: str
    title: str
    """Title of the Series, Film or TV Station."""
    type: MetadataType
    """The type of metadata. Is it a Series, Film or LIVE TV Station?"""
    year: Optional[str] = field(default = None)
    """Year the Series or Film was released."""

    extra_func: Callable[[], Optional[ExtraMetadata]] = field(default = lambda: None)
    """Callback that returns extra metadata."""

    def get_extra(self) -> Optional[ExtraMetadata]:
        """Returns extra metadata."""
        return self.extra_func()

@dataclass
class ExtraMetadata():
    """More in-depth metadata about media."""
    description: Optional[str]
    """Description of Series, Film or TV Station."""
    image_url: Optional[str]
    """Url to high res image cover of Series, Film or TV Station."""

    alternate_titles: List[str]

    cast: List[str] | None = field(default = None)
    genres: List[str] | None = field(default = None)

    airing: AiringType | None = field(default = None)