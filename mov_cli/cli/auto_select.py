from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Iterable, TypeVar

    T = TypeVar("T")

__all__ = (
    "auto_select_choice",
)

def auto_select_choice(choices: Iterable[T], auto_select: int) -> Optional[T]:

    if auto_select == 0:
        auto_select = 1

    for index, choice in enumerate(choices):

        if index == auto_select - 1:
            return choice

    return None