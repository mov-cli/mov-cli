from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Generator, Any, Callable, TypeVar, Iterable, Tuple

    T = TypeVar('T')

import re
import types
import inquirer
import itertools
from inquirer.themes import Default
from devgoldyutils import Colours, LoggerAdapter

from ..iterfzf import iterfzf
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

# Checking whether there's only one choice in prompt 
# without losing performance is serious business at mov-cli. ~ Goldy 2024
def is_it_just_one_choice(choices: Iterable[T]) -> Tuple[bool, List[T] | Generator[T, Any, None]]:

    if isinstance(choices, types.GeneratorType):

        choices, unwounded_iterable = itertools.tee(choices) # nuh uh uh uh, we ain't wasting memory and speed.

        did_iter = False

        for index, _ in enumerate(choices):
            did_iter = True

            if index >= 1:
                return False, unwounded_iterable

        if did_iter is False:
            return False, unwounded_iterable

        return True, unwounded_iterable

    if len(choices) == 1:
        return True, choices

    return False, choices

def prompt(text: str, choices: List[T] | Generator[T, Any, None], display: Callable[[T], str], fzf_enabled: bool) -> T | None:
    """Prompt the user to pick from a list choices."""
    choice_picked = None

    is_just_one, choices = is_it_just_one_choice(choices)

    if is_just_one is True:
        logger.info("Skipping prompt as there is only a single choice to choose from...")
        return next(choices) if isinstance(choices, itertools._tee) else choices[0]

    if fzf_enabled:
        logger.debug("Launching fzf...")
        # We pass this in as a generator to take advantage of iterfzf's streaming capabilities.
        # You can find that explained as the second bullet point here: https://github.com/dahlia/iterfzf#key-features
        choice_picked, choices = iterfzf(
            iterable = ((display(choice), choice) for choice in choices), 
            prompt = text + ": ", 
            ansi = True
        )

    else:

        if isinstance(choices, types.GeneratorType):
            logger.debug("Converting choices to list for inquirer...")
            choices = [choice for choice in choices]

        logger.debug("Launching inquirer (fallback ui)...")
        choice_picked = inquirer.prompt(
            questions = [inquirer.List("choices", message = text, choices = [display(x) for x in choices])], 
            theme = MovCliTheme()
        )["choices"]

    # Using this to remove ansi colours returned in the picked choice.
    ansi_remover = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') 

    for choice in choices:
        if choice_picked is None:
            return None

        if ansi_remover.sub('', choice_picked) == ansi_remover.sub('', display(choice)):
            return choice

    return None