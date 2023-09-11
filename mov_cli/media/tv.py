from __future__ import annotations

from .media import Media

__all__ = ("TV",)

class TV(Media):
    """Represents a TV Station."""
    def __init__(
        self, 
        url: str, 
        title: str, 
        referrer: str, 
    ) -> None:

        super().__init__(
            url, title, referrer
        )