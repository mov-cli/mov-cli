import click
from pyfzf import FzfPrompt

from .. import utils

fzf = FzfPrompt()

@click.group(invoke_without_command = True)
def mov_cli():
    click.echo(utils.welcome_msg())