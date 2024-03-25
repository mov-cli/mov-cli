from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal, Tuple, List, Dict, NoReturn

import random
import getpass
from datetime import datetime
from devgoldyutils import Colours

from ..logger import mov_cli_logger
from .. import __version__ as mov_cli_version
from ..utils import  what_platform, update_available

__all__ = (
    "greetings", 
    "welcome_msg", 
    "steal_scraper_args",
    "handle_internal_plugin_error"
)

def greetings() -> Tuple[Literal["Good Morning", "Good Afternoon", "Good Evening", "Good Night"], str]:
    now = datetime.now()
    user_name = random.choice(
        ("buddy", "comrade", "co-worker", "human", "companion", "specimen")
    )

    p = now.strftime("%p")
    i = int(now.strftime("%I"))

    try:
        user_name = user_name if what_platform() == "Android" else getpass.getuser()
    except Exception as e:  # NOTE: Apparently an exception is raised but they don't tell us what exception :(
        mov_cli_logger.debug(
            "getpass couldn't get the user name so a random one is being returned. "
            f"\nError >> {e}"
        )

    greeting = None

    if p == "AM":
        if i <= 6 or i == 12:
            greeting = "Good Night"
        else:
            greeting = "Good Morning"
    else:
        if i <= 5:
            greeting = "Good Afternoon"
        elif i > 5 and i <= 8:
            greeting = "Good Evening"
        elif i > 8:
            greeting = "Good Night"

    return greeting, user_name

# This function below is inspired by animdl: https://github.com/justfoolingaround/animdl
def welcome_msg(display_hint: bool = False, display_version: bool = False) -> str:
    """Returns cli welcome message."""
    now = datetime.now()
    adjective = random.choice(
        ("gorgeous", "wonderful", "beautiful", "magnificent")
    )

    greeting, user_name = greetings()

    text = f"\n{greeting}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}{adjective} {Colours.PINK_GREY}%A! {Colours.RESET}"
    )

    if display_hint is True and display_version is False:
        text += f"\n\n- Hint: {Colours.CLAY}mov-cli {Colours.PINK_GREY}-s films {Colours.ORANGE}mr.robot{Colours.RESET}" \
            f"\n- Hint: {Colours.CLAY}mov-cli {Colours.PINK_GREY}-s anime {Colours.ORANGE}chuunibyou demo take on me{Colours.RESET}"

    if display_version is True:
        text += f"\n\n{Colours.CLAY}-> {Colours.RESET}Version: {Colours.BLUE}{mov_cli_version}{Colours.RESET}"

    if update_available():
        text += f"\n\n {Colours.PURPLE}ツ {Colours.ORANGE}An update is available! --> {Colours.RESET}pip install mov-cli -U"

    return text + "\n"

def steal_scraper_args(query: List[str]) -> Dict[str, bool]:
    scrape_arguments = [x for x in query if "--" in x]

    mov_cli_logger.debug(f"Scraper args picked up on --> {scrape_arguments}")

    for scrape_arg in scrape_arguments:
        query.remove(scrape_arg)

    return dict(
        [(x.replace("--", ""), True) for x in scrape_arguments]
    )

def handle_internal_plugin_error(e: Exception) -> NoReturn:
    mov_cli_logger.critical(
        "An error occurred inside a plugin. This is most likely nothing to do with mov-cli, " \
            f"make sure your plugins are up to date! \nError: {e}"
    )

    raise e