from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from typing import Literal, List, Type
    from ..scraper import Scraper

import random
import getpass
from datetime import datetime
from devgoldyutils import Colours

from .. import utils, scrapers
from .. import __version__ as mov_cli_version

__all__ = ()

SCRAPERS: List[Scraper] = [
    scrapers.Sflix,
    scrapers.Gogoanime,
    scrapers.RemoteStream
]

def greetings() -> Literal["Good Morning", "Good Afternoon", "Good Evening", "Good Night"]:
    now = datetime.now()
    p = now.strftime("%p")
    i = int(now.strftime("%I"))

    if p == "AM":
        if i >= 6:
            return "Good Morning"
        else:
            return "Good Night"
    else:
        if i <= 5:
            return "Good Afternoon"
        elif i > 5 and i <= 8:
            return "Good Evening"
        elif i > 8:
            return "Good Night"

def welcome_msg(logger: logging.Logger, display_hint: bool = False, display_version: bool = False) -> str: # Inspired by animdl: https://github.com/justfoolingaround/animdl
    """Returns cli welcome message."""
    now = datetime.now()
    user_name = random.choice(
        ("buddy", "comrade", "co-worker", "human", "companion", "specimen")
    )
    adjective = random.choice(
        ("gorgeous", "wonderful", "beautiful", "magnificent")
    )

    try:
        user_name = getpass.getuser()
    except (
        Exception
    ) as e:  # NOTE: Apparently an exception is raised but they don't tell us what exception :(
        logger.debug(
            "getpass couldn't get the user name so a random one is being returned. "
            f"\nError >> {e}"
        )

    text = f"\n{greetings()}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}{adjective} {Colours.PINK_GREY}%A! {Colours.RESET}"
    )

    if display_hint is True and display_version is False:
        text += f"\n\n- Hint: {Colours.CLAY}mov-cli {Colours.ORANGE}spider man no way home{Colours.RESET}"

    if display_version is True:
        text += f"\n\n{Colours.CLAY}-> {Colours.RESET}Version: {Colours.BLUE}{mov_cli_version}{Colours.RESET}"

    if utils.update_available():
        text += f"\n\n {Colours.PURPLE}ツ {Colours.ORANGE}An update is available! --> {Colours.RESET}pip install mov-cli -U"

    return text

def get_scraper(provider: str) -> Type[Scraper]:

    for scraper in SCRAPERS:

        if provider.lower() == scraper.__name__.lower():
            return scraper

    raise ValueError(
        f"Could not find the provider '{provider}'! Make sure to check for typos."
    )