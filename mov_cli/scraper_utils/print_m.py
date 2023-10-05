from __future__ import annotations
from typing import TYPE_CHECKING

from devgoldyutils import pprint

if TYPE_CHECKING:
    from ..media import Metadata

def print_metadata(metadata: Metadata):
    # TODO: You can pretty print metadata like normal btw if you just want a representation of it, so I would say remove this. ~ Goldy
    DICT = {}

    DICT["title"] = metadata.title
    DICT["id"] = metadata.id
    DICT["url"] = metadata.url
    DICT["image_url"] = metadata.image_url
    DICT["year"] = metadata.year
    DICT["genre"] = metadata.genre
    DICT["cast"] = metadata.cast
    DICT["description"] = metadata.description

    pprint(DICT)