import click
from pyfzf import FzfPrompt

from .. import utils
from .. import Media
from .. import MPV, Player
from ..provider import RemoteStream

fzf = FzfPrompt()

def test():
    rs = RemoteStream()
    a = rs.search("The Grand Tour")
    print(a)
    rs.select(1)
    seasons = rs.getSeasons()
    episodes = rs.getEpisodes(1)
    print(seasons, episodes)
    a = rs.getMedia(1, 1)
    print(a.url)

@click.group(invoke_without_command=True)
def mov_cli():
    click.echo(utils.welcome_msg())
    test()