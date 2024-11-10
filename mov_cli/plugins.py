"""
Module containing mov-cli plugin related stuff.
"""
from __future__ import annotations
from typing_extensions import NotRequired
from typing import TYPE_CHECKING, TypedDict, TypeVar, Union

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Optional, Dict, List, Tuple, Literal, Type

    from .utils.platform import SUPPORTED_PLATFORMS

import importlib
from dataclasses import dataclass
from devgoldyutils import LoggerAdapter

from .scraper import Scraper
from .logger import mov_cli_logger

__all__ = (
    "Plugin",
    "load_plugin",
    "V1PluginHookDataT",
    "V2PluginHookDataT",
)

logger = LoggerAdapter(mov_cli_logger, prefix = "Plugins")

T = TypeVar("T", int, str, bool)

class V2PluginHookDataT(TypedDict):
    """
    ⭐ Example:
    -------------
    This is how you can define the plugin hook inside your plugin::

        # my_plugin/__init__.py

        from __future__ import annotations
        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from mov_cli.plugins import V2PluginHookDataT

        from .my_scraper import MyScraper
        from .ananas_amazing_scraper import TheAnanasScraper

        plugin: V2PluginHookDataT = {
            "version": 2,
            "package_name": "my-plugin-package", # The PYPI name of your package. Set as None, if you don't have one yet.
            "scrapers": {
                "my-scraper": MyScraper,
                "ananas": TheAnanasScraper,
            },
            "scraper_configs": {
                "ananas": {
                    "unsupported_platforms": ["android", "ios"]
                }
            }
        }

        __version__ = "1.0.0"
    """
    version: Literal[2]
    package_name: str
    """The name of the pypi package. This is required for the plugin update notifier to work."""
    scrapers: Dict[str, Type[Scraper]]
    """
    Where you define the IDs of the scraper classes your plugin has to offer.
    The default scraper is always the first scraper that is defined in the dictionary.
    Scrapers should ideally be put in order of which is best / recommended, if one scraper fails and
    the user has "try next scraper" mode enabled, the next scraper in that exact order will be invoked.

    .. Warning::

        In version 2 the "DEFAULT" keys should no longer be present!
    """
    scraper_configs: Dict[str, ScraperConfigT]

class V1PluginHookDataT(TypedDict):
    version: Literal[1]
    package_name: str
    """The name of the pypi package. This is required for the plugin update notifier to work."""
    scrapers: Dict[str, Type[Scraper]] | PluginHookScrapersT
    args: Dict[str, Type[T]]

# NOTE: Here for backwards compatibility with pre-v4.5 plugins.
PluginHookData = V1PluginHookDataT

PluginHookDataUnionT = Union[V1PluginHookDataT, V2PluginHookDataT]

class ScraperConfigT(TypedDict):
    allowed_args: NotRequired[Dict[str, Type[T]]]
    unsupported_platforms: List[SUPPORTED_PLATFORMS]

PluginHookScrapersT = TypedDict(
    "PluginHookScrapersT",
    {
        "DEFAULT": Scraper,
        "LINUX.DEFAULT": Scraper,
        "ANDROID.DEFAULT": Scraper,
        "IOS.DEFAULT": Scraper,
        "WINDOWS.DEFAULT": Scraper,
        "DARWIN.DEFAULT": Scraper
    }
)

@dataclass
class Plugin:
    module: ModuleType
    hook_data: PluginHookDataUnionT

    @property
    def scrapers(self) -> List[Tuple[str, Type[Scraper]]]:
        if self.hook_data["version"] == 2:
            return [
                (scraper[0], scraper[1]) for scraper in self.hook_data.get("scrapers", []).items()
            ]

        non_default_scrapers = []

        for scraper_namespace, scraper_class in self.hook_data["scrapers"].items():

            if scraper_namespace.endswith("DEFAULT"):
                continue

            non_default_scrapers.append((scraper_namespace, scraper_class))

        return non_default_scrapers

    @property
    def version(self) -> Optional[str]:
        return getattr(self.module, "__version__", None)

    def default_scraper(self, platform: SUPPORTED_PLATFORMS) -> Optional[Scraper]:
        if self.hook_data["version"] == 2:
            # Default scraper in version 2 plugin hook is just the first scraper defined.
            return next(
                self.hook_data.get("scrapers", []).values(), None
            )

        for scraper_namespace, scraper_class in self.hook_data.get("scrapers").items():

            if scraper_namespace == f"{platform}.DEFAULT" or scraper_namespace == "DEFAULT":
                return scraper_class

        return None

def load_plugin(module_name: str) -> Optional[Plugin]:
    try:
        plugin_module = importlib.import_module(module_name.replace("-", "_"))
    except ModuleNotFoundError as e:
        logger.error(f"Failed to import a plugin from the module '{module_name}'! Error --> {e}")
        return None

    plugin_data: Optional[PluginHookData] = getattr(plugin_module, "plugin", None)

    if plugin_data is None:
        logger.warning(f"Failed to load the plugin '{module_name}'! It doesn't contain a plugin hook!")
        return None

    return Plugin(
        module = plugin_module,
        hook_data = plugin_data
    )