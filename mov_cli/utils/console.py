from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging

import random
import getpass
from datetime import datetime
from devgoldyutils import Colours
from httpx import get

import mov_cli

def update_available() -> bool:
    pypi = get("https://pypi.org/pypi/mov-cli/json").json()
    pypi_ver = pypi["info"]["version"]

    if pypi_ver > mov_cli.__version__:
        return True

    return False

def welcome_msg(logger: logging.Logger) -> str: # Inspired by animdl: https://github.com/justfoolingaround/animdl
    """Returns cli welcome message."""
    now = datetime.now()
    user_name = random.choice(
        ("buddy", "comrade", "co-worker", "human", "companion", "specimen")
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

    greetings = random.choice(("Hello", "Welcome", "Greetings"))

    text = f"{greetings}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}gorgeous {Colours.PINK_GREY}%A!{Colours.RESET}" # removed 
    )

    if update_available():
        text += "\n       An update is available! --> pip install mov-cli -U"

    return text
