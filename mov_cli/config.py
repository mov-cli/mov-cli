from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .players import Player
    from typing import Type, Dict

import os
import toml
import platformdirs
from pathlib import Path

from . import players

__all__ = ("Config",)

class Config():
    """Class that wraps the mov-cli configuration file."""
    def __init__(self, config_path: Path = None) -> None:
        mov_cli_data_path = platformdirs.site_data_dir("mov_cli", ensure_exists = True) # TODO: I might make platformdirs more accessible in the future. I'm not sure yet.

        if config_path is None:
            config_path = Path.joinpath(mov_cli_data_path, "mov_cli.toml")

        if not config_path.exists():
            config_file = open(config_path, "w")

            with open(f"{Path(os.path.split(__file__)[0]).parent}{os.sep}mov_cli.template.toml", "r") as config_file_template:
                config_file.write(config_file_template)

            config_file.close()

        self.data: Dict[str, str | bool | int] = toml.load(config_path)

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
    def dl_location(self) -> str:
        """Returns download loaction. Defaults to OS's Download loaction."""
        return self.data.get("dl_loaction", platformdirs.user_downloads_dir())

