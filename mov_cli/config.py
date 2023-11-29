from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, final

if TYPE_CHECKING:
    from .players import Player
    from typing import Dict, Union, Literal, Any

    JSON_VALUES = Union[str, bool, int, dict]
    SUPPORTED_PARSERS = Literal["lxml", "html.parser"]

import os
import toml
import platformdirs
from pathlib import Path
from importlib.util import find_spec
from devgoldyutils import LoggerAdapter

from . import players, mov_cli_logger

__all__ = ("Config",)

@final
class ConfigUIData(TypedDict):
    fzf: bool

@final
class ConfigHTTPData(TypedDict):
    headers: Dict[str, str]

@final
class ConfigDownloadsData(TypedDict):
    save_path: str

@final
class ProviderData(TypedDict):
    default: str

@final
class ConfigData(TypedDict):
    debug: bool
    player: str
    flatpak_mpv: bool
    parser: SUPPORTED_PARSERS
    ui: ConfigUIData
    http: ConfigHTTPData
    downloads: ConfigDownloadsData
    provider: ProviderData

class Config():
    """Class that wraps the mov-cli configuration file. Mostly used under the CLI interface."""
    def __init__(self, override_config: ConfigData = None, config_path: Path = None) -> None:
        self.config_path = config_path
        self.logger = LoggerAdapter(mov_cli_logger, prefix = "Config")

        self.data: ConfigData = {}

        if override_config is None:
            template_config_path = f"{Path(os.path.split(__file__)[0])}{os.sep}config.template.toml"
            # TODO: I might make platformdirs more accessible in the future. I'm not sure yet.
            mov_cli_data_path = platformdirs.site_data_dir("mov_cli", ensure_exists = True)

            if self.config_path is None:
                self.config_path = Path.joinpath(Path(mov_cli_data_path), "config.toml")

            if not self.config_path.exists():
                self.logger.debug("The 'config.toml' file doesn't exist so we're creating it...")
                config_file = open(self.config_path, "w")

                with open(template_config_path, "r") as config_template:
                    config_file.write(config_template.read())

                config_file.close()
                self.logger.info(f"Config created at '{self.config_path}'.")

            self.data = toml.load(self.config_path).get("mov-cli", {})

        else:
            self.data = override_config

    @property
    def player(self) -> Player:
        """Returns the configured player class. Defaults to MPV."""
        value = self.data.get("player", "mpv")

        if value.lower() == "mpv":
            return players.MPV(self)
        elif value.lower() == "vlc":
            return players.VLC(self)

        return players.CustomPlayer(self, value)

    @property
    def provider(self) -> str:
        """Returns the provider that should be used to scraper by default."""
        return self.data.get("provider", {}).get("default", "sflix")

    @property
    def flatpak_mpv(self) -> bool:
        """Returns whether we should use the flatpak version of mpv on Linux."""
        return self.data.get("flatpak_mpv", False)

    @property
    def fzf_enabled(self) -> bool:
        """Returns whether fzf is allowed to be used."""
        return self.data.get("ui", {}).get("fzf", True)

    @property
    def parser(self) -> SUPPORTED_PARSERS | Any:
        """Returns the parser type configured by the user else it just returns the default."""
        default_parser = "lxml" if find_spec("lxml") else "html.parser"
        return self.data.get("parser", default_parser)

    @property
    def download_location(self) -> str:
        """Returns download location. Defaults to OS's download location."""
        default_location = platformdirs.user_downloads_dir()
        return self.data.get("downloads", {}).get("save_path", default_location)

    @property
    def debug(self) -> bool:
        """Returns whether debug should be enabled or not."""
        return self.data.get("debug", False)

    @property
    def proxy(self) -> dict | None:
        """Returns proxy data. Defaults to None"""
        proxy_config = self.data.get("proxy")

        if proxy_config is not None:
            proxy = None

            username = proxy_config.get("username")
            password = proxy_config.get("password")

            scheme = proxy_config.get("scheme")
            ip = proxy_config.get("ip")
            port = proxy_config.get("port")

            if username and password:
                proxy = f"{scheme}://{username}:{password}@{ip}:{port}"
            else:
                proxy = f"{scheme}://{ip}:{port}"

            return {"all://": proxy}
        else:
            return None

    @property
    def http_headers(self) -> dict:
        """Returns http headers."""
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }

        return self.data.get("http", {}).get("headers", default_headers)