from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ("EpisodeSelector",)

@dataclass
class EpisodeSelector:
    """Swift util to use when asking the scraper which episode of a show to scrape."""
    episode: int = field(default = 1)
    season: int = field(default = 1)