from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config
    from typing import List, Generator, Any, Callable, TypeVar

    T = TypeVar('T')

import re
import types
import iterfzf
import inquirer
from inquirer.themes import Default
from devgoldyutils import Colours, LoggerAdapter
from .. import errors

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

class NothingSelected(errors.MovCliException):
    """Raises when nothing is selected."""
    def __init__(self) -> None:
        super().__init__(
            "You didn't select anything",
        )

def prompt(text: str, choices: List[T] | Callable[[], Generator[T, Any, None]], display: Callable[[T], str], config: Config) -> T | None:
    """Prompt the user to pick from a list choices."""
    choice_picked: str = None
    stream_choices = choices

    print("") # Whitespace

    if isinstance(choices, list):
        stream_choices = lambda: choices

    if config.fzf_enabled:
        logger.debug("Launching fzf...")
        # We pass this in as a generator to take advantage of iterfzf's streaming capabilities.
        # You can find that explained as the second bullet point here: https://github.com/dahlia/iterfzf#key-features
        choice_picked = iterfzf.iterfzf((display(choice) for choice in stream_choices()), prompt = text + ": ", ansi = True)

    else:

        if isinstance(choices, types.GeneratorType):
            logger.debug("Converting choices to list for inquirer...")
            choices = [display(choice) for choice in stream_choices()]
            stream_choices = lambda: choices

        logger.debug("Launching inquirer (fallback ui)...")
        choice_picked = inquirer.prompt(
            [inquirer.List("choices", message = text, choices = [display(choice) for choice in stream_choices()])], theme = MovCliTheme()
        )["choices"]

    # Using this to remove ansi colours returned in the picked choice.
    ansi_remover = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') 

    # Yes I know if this is a generator I'm running it twice which is inefficient but 
    # this is the only solution I can think of to return the proper value and also 
    # retain streaming search results straight to fzf (line 42).
    for choice in stream_choices():
        if choice_picked is None:
            raise NothingSelected()
        
        if ansi_remover.sub('', choice_picked) == ansi_remover.sub('', display(choice)):
            return choice

    return None