__all__ = ("Media",)


class Media:
    """Represents any piece of media in mov-cli that can be streamed or downloaded."""

    def __init__(self, data: dict = None) -> None:
        self.data = data

    @property
    def url(self) -> str:
        return self.data.get("url")

    @property
    def title(self) -> str:
        return self.data.get("title")

    @property
    def type(self) -> str:
        return self.data.get("type")

    @property
    def referrer(self) -> str:
        return self.data.get("referrer")

    @property
    def img(self) -> dict:
        return self.data.get("img", None)

    @property
    def id(self) -> str:
        return self.data.get("id", None)

    @property
    def seasons(self) -> int:
        return self.data.get("seasons", None)

    @property
    def season(self) -> int:
        return self.data.get("season", None)

    @property
    def episode(self) -> int:
        return self.data.get("episode", None)

    @property
    def year(self) -> str:
        return self.data.get("year", None)
