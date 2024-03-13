from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from typing import Literal, Type, Optional, Any, Tuple, List, Dict
    from ..media import Metadata
    from ..scraper import Scraper
    from ..config import Config
    from ..plugins import PluginHookData

import os
import random
import getpass
from datetime import datetime
from devgoldyutils import Colours

from .ui import prompt

from .. import utils
from ..plugins import load_plugin
from ..media import MetadataType
from ..utils import EpisodeSelector, what_platform
from ..logger import mov_cli_logger
from .. import __version__ as mov_cli_version

__all__ = (
    "greetings", 
    "welcome_msg", 
    "handle_episode", 
    "get_scraper", 
    "get_plugins_data", 
    "select_scraper", 
    "set_cli_config", 
    "open_config_file"
)

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
        user_name = user_name if what_platform() == "Android" else getpass.getuser()
    except Exception as e:  # NOTE: Apparently an exception is raised but they don't tell us what exception :(
        logger.debug(
            "getpass couldn't get the user name so a random one is being returned. "
            f"\nError >> {e}"
        )

    text = f"\n{greetings()}, {Colours.ORANGE.apply(user_name)}."
    text += now.strftime(
        f"\n    It's {Colours.BLUE}%I:%M %p {Colours.RESET}on a {Colours.PURPLE}{adjective} {Colours.PINK_GREY}%A! {Colours.RESET}"
    )

    if display_hint is True and display_version is False:
        text += f"\n\n- Hint: {Colours.CLAY}mov-cli {Colours.PINK_GREY}-s films {Colours.ORANGE}mr.robot{Colours.RESET}" \
            f"\n- Hint: {Colours.CLAY}mov-cli {Colours.PINK_GREY}-s anime {Colours.ORANGE}chuunibyou demo take on me{Colours.RESET}"

    if display_version is True:
        text += f"\n\n{Colours.CLAY}-> {Colours.RESET}Version: {Colours.BLUE}{mov_cli_version}{Colours.RESET}"

    if utils.update_available():
        text += f"\n\n {Colours.PURPLE}ツ {Colours.ORANGE}An update is available! --> {Colours.RESET}pip install mov-cli -U"

    return text + "\n"

def handle_episode(episode: Optional[str], scraper: Scraper, choice: Metadata, fzf_enabled: bool) -> Optional[utils.EpisodeSelector]:
    if choice.type == MetadataType.MOVIE:
        return EpisodeSelector()

    if episode is None:
        mov_cli_logger.info(f"Scrapping episodes for '{Colours.CLAY.apply(choice.title)}'...")
        metadata_episodes = scraper.scrape_metadata_episodes(choice)

        if metadata_episodes.get(None) == 1:
            return EpisodeSelector()

        season = prompt(
            "Select Season", 
            choices = [season for season in metadata_episodes], 
            display = lambda x: f"Season {x}", 
            fzf_enabled = fzf_enabled
        )

        if season is None:
            return None

        ep = prompt(
            "Select Episode", 
            choices = [ep for ep in range(1, metadata_episodes[season])], 
            display = lambda x: f"Episode {x}",
            fzf_enabled = fzf_enabled
        )

        if ep is None:
            return None

        return EpisodeSelector(ep, season)

    episode = episode.split(":")

    if len(episode) < 2:
        mov_cli_logger.error("Incorrect episode format!")
        return False

    return utils.EpisodeSelector(episode[0], episode[1])

def get_plugins_data(plugins: Dict[str, str]) -> List[Tuple[str, str, PluginHookData]]:
    plugins_data: List[Tuple[str, str, PluginHookData]] = []

    for plugin_namespace, plugin_module_name in plugins.items():
        plugin_data = load_plugin(plugin_module_name)

        if plugin_data is None:
            continue

        plugins_data.append(
            (plugin_namespace, plugin_module_name, plugin_data)
        )

    return plugins_data

def select_scraper(plugins: Dict[str, str], fzf_enabled: bool, default_scraper: Optional[str] = None) -> Optional[Tuple[str, Type[Scraper]]]:
    plugins_data = get_plugins_data(plugins)

    if default_scraper is not None:
        scraper_name, scraper_or_available_scrapers = get_scraper(default_scraper, plugins_data)

        if scraper_name is None:
            mov_cli_logger.error(
                f"Could not find a scraper by the id '{default_scraper}'! Are you sure the plugin is installed and in your config? " \
                    "Read the wiki for more on that: 'https://github.com/mov-cli/mov-cli/wiki#plugins'." \
                    f"\n\n  {Colours.GREEN}Available Scrapers{Colours.RESET} -> {scraper_or_available_scrapers}"
            )

            return None

        return scraper_name, scraper_or_available_scrapers

    chosen_plugin = prompt(
        "Select a plugin", 
        choices = plugins_data, 
        display = lambda x: f"{Colours.ORANGE.apply(x[0])} [{Colours.PINK_GREY.apply(x[1])}]", 
        fzf_enabled = fzf_enabled
    )

    if chosen_plugin is not None:
        plugin_namespace, _, plugin_data = chosen_plugin

        chosen_scraper = prompt(
            "Select a scraper", 
            choices = [scraper for scraper in plugin_data["scrapers"].items()], 
            display = lambda x: Colours.BLUE.apply(x[0].lower()), 
            fzf_enabled = fzf_enabled
        )

        if chosen_scraper is None:
            return None

        scraper_name, scraper = chosen_scraper

        return f"{plugin_namespace}.{scraper_name}".lower(), scraper

    return None

def get_scraper(scraper_id: str, plugins_data: List[Tuple[str, str, PluginHookData]]) -> Tuple[str, Type[Scraper] | Tuple[None, List[str]]]:
    available_scrapers = []

    for plugin_namespace, _, plugin_hook_data in plugins_data:
        scrapers = plugin_hook_data["scrapers"]

        if scraper_id.lower() == plugin_namespace.lower() and "DEFAULT" in scrapers:
            return f"{plugin_namespace}.DEFAULT", scrapers["DEFAULT"]

        for scraper_name, scraper in scrapers.items():
            id = f"{plugin_namespace}.{scraper_name}".lower()

            available_scrapers.append(id)

            if scraper_id.lower() == id:
                return id, scraper

    return None, available_scrapers

def set_cli_config(config: Config, **kwargs: Optional[Any]) -> Config:
    debug = kwargs.get("debug")
    player = kwargs.get("player")
    scraper = kwargs.get("scraper")
    fzf = kwargs.get("fzf")

    if debug is not None:
        config.data["debug"] = debug

    if player is not None:
        config.data["player"] = player

    if scraper is not None:
        if config.data.get("scrapers") is None:
            config.data["scrapers"] = {}

        config.data["scrapers"]["default"] = scraper

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