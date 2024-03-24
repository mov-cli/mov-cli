from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from ..media import Metadata
    from ..scraper import Scraper

from devgoldyutils import Colours

from .ui import prompt
from .auto_select import auto_select_choice
from .utils import handle_internal_plugin_error

from ..media import MetadataType
from ..logger import mov_cli_logger

__all__ = (
    "search", 
)

def search(query: str, auto_select: Optional[int], scraper: Scraper, fzf_enabled: bool) -> Optional[Metadata]:
    choice = None

    mov_cli_logger.info(f"Searching for '{Colours.ORANGE.apply(query)}'...")

    try:
        search_results = scraper.search(query)
    except Exception as e:
        handle_internal_plugin_error(e)

    if auto_select is not None:
        choice = auto_select_choice((choice for choice in search_results), auto_select)
    else:
        choice = prompt(
            "Choose Result", 
            choices = (choice for choice in search_results), 
            display = lambda x: f"{Colours.CLAY if x.type == MetadataType.MOVIE else Colours.BLUE}{x.title}" \
                f"{Colours.RESET} ({x.year if x.year is not None else 'N/A'})", 
            fzf_enabled = fzf_enabled
        )

    return choice