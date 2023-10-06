from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple

import click
import logging

# from . import ui
from . import utils
from ..config import Config
from ..logger import mov_cli_logger

__all__ = ("mov_cli",)

@click.group(invoke_without_command = True)
@click.argument("query", nargs = -1)
@click.option("--debug", default = None, is_flag = True, help = "Enable debug logs.")
@click.option(
    "--version", "-v", 
    default = None, 
    is_flag = True, 
    help = "Tells you what version mov-cli is currently on."
)
@click.option(
    "--player", "-p", 
    default = None, 
    type = click.Choice(["mpv", "vlc"]), 
    help = "Player you would like to stream with."
)
@click.option("--fzf/--no-fzf", default = None, help = "Toggle fzf for select prompts.")
def mov_cli(query: Tuple[str], debug: bool, version: bool, player: str, fzf: bool):
    config = Config()

    if debug is not None:
        config.data["debug"] = debug

    if player is not None:
        config.data["player"] = player

    if fzf is not None:
        if config.data.get("ui") is None:
            config.data["ui"] = {}

        config.data["ui"]["fzf"] = fzf

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    print(
        utils.welcome_msg(mov_cli_logger, True if len(query) == 0 else False, version) + "\n"
    )

    mov_cli_logger.debug(f"Config -> {config.data}")

    # NOTE: Where searching will happen.
    if len(query) > 0:
        ...