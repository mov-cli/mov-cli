from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ("EpisodeSelector",)

@dataclass
class EpisodeSelector:
    """Swift util to use when interfacing scrapers to select an episode of a show."""
    episode: int = field(default = 1)
    season: int = field(default = 1)