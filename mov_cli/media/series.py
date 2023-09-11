from __future__ import annotations

from .media import Media

__all__ = ("Series",)

class Series(Media):
    """Represents a TV Show. E.g an Anime or Cartoon"""
    def __init__(
        self, 
        url: str, 
        title: str, 
        referrer: str, 
        episode: int, 
        season: int,
        subtitles: dict | None
    ) -> None:
        self.season = season
        """The season this series belongs to."""
        self.episode = episode
        """The episode number of this series."""
        self.subtitles = subtitles

        super().__init__(
            url, title, referrer
        )