from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Optional, Tuple, List, Dict
    from ..scraper import Scraper
    from ..plugins import PluginHookData

from devgoldyutils import Colours

from .ui import prompt

from ..plugins import load_plugin
from ..logger import mov_cli_logger

__all__ = (
    "get_scraper", 
    "get_plugins_data", 
    "select_scraper", 
)

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