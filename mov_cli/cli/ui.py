from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config
    from ..media import Metadata
    from typing import List, Generator, Any

import types
import iterfzf
import inquirer
from inquirer.themes import Default
from devgoldyutils import Colours, LoggerAdapter

from ..logger import mov_cli_logger

__all__ = ("prompt",)

logger = LoggerAdapter(mov_cli_logger, prefix = Colours.PURPLE.apply("prompt"))

class MovCliTheme(Default):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = Colours.BLUE.value
        self.Question.brackets_color = Colours.GREY.value
        self.List.selection_color = Colours.CLAY.value
        self.List.selection_cursor = "❯"

def prompt(text: str, choices: List[str] | Generator[Metadata, Any, None], config: Config) -> str:
    """Prompt the user to pick from a list choices."""
    if config.fzf_enabled:
        logger.debug("Launching fzf...")
        return iterfzf.iterfzf((f"{metadata.title} ({metadata.year})" for metadata in choices), prompt = text)

    if isinstance(choices, types.GeneratorType):
        logger.debug("Converting choices to list for inquirer...")
        choices = [f"{metadata.title} ({metadata.year})" for metadata in choices]

    return inquirer.prompt(
        [inquirer.List("choices", message = text, choices = choices)], theme = MovCliTheme()
    )["choices"]