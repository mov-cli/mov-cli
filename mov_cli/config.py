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

from . import players

__all__ = ("Config",)


class Config:
    """Class that wraps the mov-cli configuration file."""

    def __init__(self, config_path: Path = None) -> None:
        mov_cli_data_path = platformdirs.site_data_dir(
            "mov_cli", ensure_exists=True
        )  # TODO: I might make platformdirs more accessible in the future. I'm not sure yet.

        if config_path is None:
            config_path = Path.joinpath(mov_cli_data_path, "mov_cli.toml")

        if not config_path.exists():
            config_file = open(config_path, "w")

            with open(
                f"{Path(os.path.split(__file__)[0]).parent}{os.sep}mov_cli.template.toml",
                "r",
            ) as config_file_template:
                config_file.write(config_file_template)

            config_file.close()

        self.data: Dict[str, JSON_VALUES] = toml.load(config_path)

    @property
    def player(self) -> Type[Player]:
        """Returns the configured player class. Defaults to MPV."""
        value = self.data.get("player", "mpv")

        if value.lower() == "mpv":
            return players.MPV
        elif value.lower() == "vlc":
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
    def debug(self) -> int:
        """Returns a Logging Setting. Defaults to Logging.INFO"""
        from logging import DEBUG, INFO

        debug = self.data.get("debug")
        if debug:
            return DEBUG
        else:
            return INFO

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
