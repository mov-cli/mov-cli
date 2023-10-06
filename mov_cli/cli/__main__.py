import click
import logging
from pyfzf import FzfPrompt

from ..config import Config
from .. import utils, mov_cli_logger

fzf = FzfPrompt() # NOTE: I'll be using this later so don't worry about it sitting here.

@click.group(invoke_without_command = True)
@click.option("--debug", default = None, is_flag = True, help = "Enable debug logs.")
@click.option(
    "--player", "-p", 
    default = None, 
    type = click.Choice(['mpv', 'vlc']), 
    help = "Player you would like to stream with."
)
def mov_cli(debug: bool, player: str):
    config = Config()

    if debug is not None:
        config.data["debug"] = debug

    if player is not None:
        config.data["player"] = player

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    print(utils.welcome_msg(mov_cli_logger))