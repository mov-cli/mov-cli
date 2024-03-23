"""
Module containing mov-cli plugin related stuff.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Optional, Dict, Literal

    from .scraper import Scraper

import importlib
from devgoldyutils import LoggerAdapter

from .logger import mov_cli_logger

__all__ = (
    "load_plugin", 
    "PluginHookData"
)

logger = LoggerAdapter(mov_cli_logger, prefix = "Plugins")

class PluginHookData(TypedDict):
    version: int
    scrapers: Dict[str, Scraper] | Dict[Literal["DEFAULT"], Scraper]

def load_plugin(module_name: str) -> Optional[PluginHookData]:
    try:
        plugin_module = importlib.import_module(module_name.replace("-", "_"))
    except ModuleNotFoundError as e:
        logger.error(f"Failed to import a plugin from the module '{module_name}'! Error --> {e}")
        return None

    plugin_data = getattr(plugin_module, "plugin", None)

    if plugin_data is None:
        logger.warning(f"Failed to load the plugin '{module_name}'! It doesn't contain a plugin hook!")

    return plugin_data