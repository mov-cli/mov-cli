import random
import getpass
from datetime import datetime
from devgoldyutils import Colours

from ..logger import mov_cli_logger

def welcome_msg() -> str: # Inspired by animdl: https://github.com/justfoolingaround/animdl
    """Returns cli welcome message."""
    now = datetime.now()
    user_name = random.choice(("buddy", "comrade", "co-worker", "human", "companion"))

    try:
        user_name = getpass.getuser()
    except Exception as e: # NOTE: Apparently an exception is raised but they don't tell us what exception :(
        mov_cli_logger.debug(
            "getpass couldn't get the user name so a random one is being returned. " \
            f"\nError >> {e}"
        )

    greetings = random.choice(("Hello", "Welcome", "Greetings"))

    text = f"  {greetings}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    ╰┈➤ It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}gorgeous {Colours.PINK_GREY}%A!{Colours.RESET}"
    )

    return text