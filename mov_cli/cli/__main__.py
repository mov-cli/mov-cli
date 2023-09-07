import click
from pyfzf import FzfPrompt

from .. import utils

fzf = FzfPrompt() # NOTE: I'll be using this later so don't worry about it sitting here.

@click.group(invoke_without_command = True)
def mov_cli():
    click.echo(utils.welcome_msg())
    #test()