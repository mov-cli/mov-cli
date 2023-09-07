from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .players import Player
    from typing import Type, Dict, Union

    JSON_VALUES = Union[str, bool, int, dict]

import os
import toml
import platformdirs
from pathlib import Path
from devgoldyutils import LoggerAdapter

from . import players, mov_cli_logger

__all__ = ("Config",)


class Config():
    """Class that wraps the mov-cli configuration file. Mostly used under the CLI interface."""
    def __init__(self, config_path: Path = None) -> None:
        self.config_path = config_path
        self.logger = LoggerAdapter(mov_cli_logger, prefix = "Config")

        template_config_path = f"{Path(os.path.split(__file__)[0])}{os.sep}mov_cli.template.toml"
        # TODO: I might make platformdirs more accessible in the future. I'm not sure yet.
        mov_cli_data_path = platformdirs.site_data_dir("mov_cli", ensure_exists = True)

        if self.config_path is None:
            self.config_path = Path.joinpath(Path(mov_cli_data_path), "mov_cli.toml")

        if not self.config_path.exists():
            self.logger.debug("The 'mov-cli.toml' config doesn't exist so we're creating it...")
            config_file = open(self.config_path, "w")

            with open(template_config_path, "r") as config_template:
                config_file.write(config_template.read())

            config_file.close()
            self.logger.debug(f"Config created at '{self.config_path}'.")

        self.data: Dict[str, JSON_VALUES] = toml.load(self.config_path).get("mov-cli", {})

    @property
    def player(self) -> Type[Player]:
        """Returns the configured player class. Defaults to MPV."""
        value = self.data.get("player", "mpv").lower()

        if value == "mpv":
            return players.MPV
        elif value == "vlc":
            return players.VLC

        return players.MPV

    @property
    def flatpak_mpv(self) -> bool:
        """Returns whether we should use the flatpak version of mpv on Linux."""
        return self.data.get("flatpak_mpv", False)

    @property
    def download_location(self) -> str:
        """Returns download location. Defaults to OS's download location."""
        default_location = platformdirs.user_downloads_dir()
        downloads_config = self.data.get("downloads")

        if downloads_config is not None:
            return downloads_config.get("download_location", default_location)

        return default_location

    @property
    def debug(self) -> bool:
        """Returns whether debug should be enabled or not."""
        return self.data.get("debug", False)

    @property
    def proxy(self) -> dict or None:
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