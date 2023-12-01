from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...media import Metadata

from enum import Enum
from ...media import MetadataType

__all__ = ("Fuzzy", "FuzzyMatch",)

class FuzzyMatch(Enum):
    FAIL = 0
    MATCH = 1

class Fuzzy:
    def __init__(self):
        ...

    def check_score(self, metadata: Metadata, name: str, year: str = None, type: str = None, match: int = 80) -> int:
        score = 0
        TYPE = None

        type = type.lower()
        if type == "tv" or type == "show":
            TYPE = MetadataType.SERIES
        else:
            TYPE = MetadataType.MOVIE

        if name == metadata.title:
            score += 33

        if TYPE == metadata.type:
            score += 33
        
        if year == metadata.year:
            score += 33 
    
        if score >= match:
            return FuzzyMatch.MATCH
        else:
            return FuzzyMatch.FAIL