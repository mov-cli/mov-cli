from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

import typer
import logging
from typing import List, Union
from devgoldyutils import Colours

from . import ui
from . import utils
#from ..players import MPV, VLC
from ..config import Config
# from ..scrapers import Sflix
from ..media import MetadataType
from ..logger import mov_cli_logger
from ..http_client import HTTPClient

__all__ = ("mov_cli",)

def mov_cli(
    query: Union[List[str], None] = typer.Argument(None, help = "The film, tv show or anime you would like to Query."), 
    debug: bool = typer.Option(None, help = "Enable extra logging details."), 
    version: bool = typer.Option(None, "--version", help = "Display what version mov-cli is currently on."), 
    player: str = typer.Option(None, help = "Player you would like to stream with. E.g. mpv, vlc"), 
    provider: str = typer.Option(None, help = "Provider you would like to stream from. E.g. RemoteStream, Sflix"), 
    fzf: bool = typer.Option(None, help = "Toggle fzf on/off for all user selection prompts.")
):
    config = Config()

    if debug is not None:
        config.data["debug"] = debug

    if player is not None:
        config.data["player"] = player

    if provider is not None:
        if config.data.get("provider") is None:
            config.data["provider"] = {}

        config.data["provider"]["default"] = provider

    if fzf is not None:
        if config.data.get("ui") is None:
            config.data["ui"] = {}

        config.data["ui"]["fzf"] = fzf

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    print(
        utils.welcome_msg(mov_cli_logger, True if len(query) == 0 else False, version)
    )

    mov_cli_logger.debug(f"Config -> {config.data}")

    # NOTE: Where searching will happen.
    if len(query) > 0:
        query: str = " ".join(query)
        http_client = HTTPClient(config)
        scraper = utils.get_scraper(config.provider)
        scraper = scraper(config, http_client)

        choice = ui.prompt(
            "Choose Result", 
            choices = scraper.search(query), 
            display = lambda x: f"{Colours.CLAY if x.type == MetadataType.MOVIE else Colours.BLUE}{x.title}" \
                f"{Colours.RESET} ({x.year if x.year is not None else 'N/A'})", 
            config = config
        )

        # TODO: Ask for episode if episode/season parameter is None.

        media = scraper.scrape(choice)

        # NOTE: This is all a work in progress.

        popen = config.player.play(media) 
        popen.wait()

def app():
    typer.run(mov_cli)