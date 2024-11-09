from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        List, Tuple, Optional, TypeVar, Literal
    )

    T = TypeVar("T")

    from ..utils.platform import SUPPORTED_PLATFORMS

import os
import json
import random
import getpass
from pathlib import Path
from datetime import datetime
from devgoldyutils import Colours, LoggerAdapter

import mov_cli

from ..cache import Cache
from ..logger import mov_cli_logger
from ..utils import  what_platform, update_available, plugin_update_available, update_command

__all__ = ()

logger = LoggerAdapter(mov_cli_logger, prefix = "greetings")

# This function below is inspired by animdl: https://github.com/justfoolingaround/animdl
def get_welcome_message(
    plugins: List[Plugin],
    platform: SUPPORTED_PLATFORMS,
    check_for_updates: bool = False,
    display_tip: bool = False,
    display_version: bool = False
) -> str:
    """Returns cli welcome message as a coloured and formatted string."""
    now = datetime.now()
    mov_cli_path = Path(os.path.split(__file__)[0])
    adjective = random.choice(
        ("gorgeous", "wonderful", "beautiful", "magnificent")
    )

    greeting, user_name = get_greetings()

    text = f"\n{greeting}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}{adjective} {Colours.PINK_GREY}%A! {Colours.RESET}"
    )

    if display_tip and display_version is False:

        if random.randint(0, 1) == 0:
            text += f"\n\n- {Colours.BLUE}Hint: {Colours.RESET}mov-cli {Colours.PINK_GREY}-s films {Colours.ORANGE}mr.robot{Colours.RESET}" \
                f"\n- {Colours.BLUE}Hint: {Colours.RESET}mov-cli {Colours.PINK_GREY}-s anime {Colours.ORANGE}chuunibyou demo take on me{Colours.RESET}"

        else:
            random_tip = get_random_tip()
            text += f"\n\n- {Colours.ORANGE}TIP: {Colours.RESET}{random_tip}"

    if display_version is True:
        text += f"\n\n{Colours.CLAY}-> {Colours.RESET}Version: {Colours.BLUE}{mov_cli.__version__}{Colours.RESET}"

    if check_for_updates:
        cache = Cache(platform, section = "update_checker")

        if update_available(cache):
            update = update_command(mov_cli_path)
            text += f"\n\n {Colours.PURPLE}ツ {Colours.ORANGE}An update is available! --> {Colours.RESET}{update}"

        plugin_needs_updating, plugins_to_update = plugin_update_available(cache, plugins)

        if plugin_needs_updating:
            update = update_command(mov_cli_path, plugins_to_update)
            text += f"\n\n {Colours.ORANGE}|˶˙ᵕ˙ )ﾉﾞ {Colours.GREEN}Some plugins need updating! --> {Colours.RESET}{update}"

    return text + "\n"

def get_random_tip(mov_cli_path: Path, platform: SUPPORTED_PLATFORMS) -> str:
    random_tips_path = mov_cli_path.joinpath("random_tips.json")

    cache = Cache(platform)
    random_tips_list: Optional[list] = cache.get_cache("random_tips")

    if random_tips_list is None:
        random_tips_list = cache.set_cache(
            "random_tips", json.load(random_tips_path.open("r")), 60 * 60 * 24 * 3 # 3 days
        )

    return random.choice(random_tips_list)

def get_greetings() -> Tuple[Literal["Good Morning", "Good Afternoon", "Good Evening", "Good Night"], str]:
    """
    Returns "good morning", "good afternoon", "good night" greetings depending on the current 
    time and the systems's username or a random name if the systems's username is not available.
    """
    now = datetime.now()
    user_name = random.choice(
        ("buddy", "comrade", "co-worker", "human", "companion", "specimen")
    )

    p = now.strftime("%p")
    i = int(now.strftime("%I"))

    try:
        user_name = user_name if what_platform() in ["Android", "iOS"] else getpass.getuser()
    except Exception as e:  # NOTE: Apparently an exception is raised but they don't tell us what exception :(
        logger.debug(
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
        if i <= 5 or i == 12:
            greeting = "Good Afternoon"
        elif i > 5 and i <= 8:
            greeting = "Good Evening"
        elif i > 8:
            greeting = "Good Night"

    return greeting, user_name