from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from ..utils import EpisodeSelector

from abc import abstractmethod

__all__ = (
    "Media", 
    "Series", 
    "Movie"
)

class Media():
    """Represents any piece of media in mov-cli that can be streamed or downloaded."""
    def __init__(self, url: str, title: str, referrer: Optional[str]) -> None:
        self.url = url
        """The stream-able url."""
        self.title = title
        """A title to represent this stream-able media."""
        self.referrer = referrer
        """The required referrer for streaming the media content."""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """The title that should be displayed by the player."""
        ...

class Series(Media):
    """Represents a TV Show. E.g an Anime or Cartoon."""
    def __init__(
        self, 
        url: str, 
        title: str, 
        referrer: Optional[str], 
        episode: EpisodeSelector, 
        subtitles: Optional[dict]
    ) -> None:
        self.episode = episode
        """The episode and season of this series."""
        self.subtitles = subtitles

        super().__init__(
            url, title, referrer
        )

    @property
    def display_name(self) -> str:
        return f"{self.title} - S{self.episode.season} EP{self.episode.episode}"

class Movie(Media):
    """Represents a Film/Movie."""
    def __init__(
        self, 
        url: str,
        title: str,
        referrer: str,
        year: Optional[str],
        subtitles: Optional[dict]
    ) -> None:
        self.year = year
        """The year this film was released."""
        self.subtitles = subtitles

        super().__init__(
            url, title, referrer
        )

    @property
    def display_name(self) -> str:
        return f"{self.title} ({self.year})"


# class LiveTV(Media):
#     """Represents media that is live, like a tv channel or a live stream."""
#     def __init__(
#         self, 
#         url: str, 
#         title: str, 
#         referrer: str, 
#     ) -> None:

#         super().__init__(
#             url, title, referrer
#         )