import click
import logging
from pyfzf import FzfPrompt

from .. import utils, mov_cli_logger
from ..config import Config

fzf = FzfPrompt() # NOTE: I'll be using this later so don't worry about it sitting here.

@click.group(invoke_without_command = True)
def mov_cli():
    config = Config()

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    click.echo(utils.welcome_msg(mov_cli_logger))
    #test()