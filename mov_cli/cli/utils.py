from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from typing import Literal, Type, Optional, Any, Tuple
    from ..scraper import Scraper
    from ..config import Config

import os
import random
import getpass
import importlib
from datetime import datetime
from devgoldyutils import Colours

from .. import utils, errors
from .. import __version__ as mov_cli_version

__all__ = ()

def greetings() -> Literal["Good Morning", "Good Afternoon", "Good Evening", "Good Night"]:
    now = datetime.now()
    p = now.strftime("%p")
    i = int(now.strftime("%I"))

    if p == "AM":
        if i <= 6 or i == 12:
            return "Good Night"
        else:
            return "Good Morning"
    else:
        if i <= 5:
            return "Good Afternoon"
        elif i > 5 and i <= 8:
            return "Good Evening"
        elif i > 8:
            return "Good Night"

# This function below is inspired by animdl: https://github.com/justfoolingaround/animdl
def welcome_msg(logger: logging.Logger, display_hint: bool = False, display_version: bool = False) -> str:
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

    return text + "\n"

# TODO: We should probably stick to one name instead of using provider and scraper interchangeably.
def get_scraper(provider_name: str, config: Config) -> Type[Tuple[str, Scraper]]:

    for _, plugin_module_name in config.plugins.items():
        # TODO: Make this plugin loading stuff a separate util method.
        plugin_module = importlib.import_module(plugin_module_name.replace("-", "_"))

        scrapers = plugin_module.plugin["scrapers"]

        for scraper_name, scraper in scrapers.items():

            if provider_name.lower() == scraper_name:
                return scraper_name, scraper

    raise errors.ProviderNotFound(provider_name)

def set_cli_config(config: Config, **kwargs: Optional[Any]) -> Config:
    debug = kwargs.get("debug")
    player = kwargs.get("player")
    provider = kwargs.get("provider")
    fzf = kwargs.get("fzf")

    if debug is not None:
        config.data["debug"] = debug

    if player is not None:
        config.data["player"] = player

    if provider is not None:
        if config.data.get("provider") is None:
            config.data["provider"] = {}

        config.data["provider"]["default"] = provider

    if fzf is not None:
        if config.data.get("ui") is None:
            config.data["ui"] = {}

        config.data["ui"]["fzf"] = fzf

    return config

def open_config_file(config: Config):
    """Opens the config file in the respectable editor for that platform."""
    editor = config.editor

    if editor is None:
        platform = utils.what_platform()

        if platform == "Windows":
            editor = "notepad"
        elif platform == "Darwin": # TODO: Implement MacOS and iOS.
            ...
        elif platform == "iOS":
            ...
        elif platform == "Linux" or platform == "Android":
            editor = "nano"

    os.system(f"{editor} {config.config_path}")