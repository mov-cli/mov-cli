from __future__ import annotations

from enum import Enum
from dataclasses import dataclass

__all__ = ("MetadataType", "Metadata")

class MetadataType(Enum):
    SERIES = 0
    MOVIE = 1
    LIVE_TV = 2

@dataclass
class Metadata:
    """Search metadata from TheTvDB."""
    id: str | None
    title: str
    """Title of the Series, Film or TV Station."""
    description: str
    """Description of Series, Film or TV Station."""
    type: MetadataType
    """The type of metadata. Is it a Series, Film or LIVE TV Station?"""
    year: str | None
    """Year the Series or Film was released."""
    image_url: str | None
    """Url to high res image cover of Series, Film or TV Station."""

    #alternate_titles: List[str]

    #cast: List[str] | None = field(default = None)
    #genre: List[str] | None = field(default = None)