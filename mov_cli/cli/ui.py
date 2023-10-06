from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from ..config import Config

import inquirer
from iterfzf import iterfzf
from devgoldyutils import Colours
from inquirer.themes import Default

__all__ = ("prompt",)

class MovCliTheme(Default):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = Colours.BLUE.value
        self.Question.brackets_color = Colours.GREY.value
        self.List.selection_color = Colours.CLAY.value
        self.List.selection_cursor = "❯"

def prompt(text: str, choices: List[str], config: Config) -> str:
    """Prompt the user to pick from a list choices."""
    if config.fzf_enabled:
        return iterfzf(choices, prompt = text)

    return inquirer.prompt(
        [inquirer.List("choices", message = text, choices = choices)], theme = MovCliTheme()
    )["choices"]