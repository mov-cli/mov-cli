from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..scraper import Scraper
    from ..utils import EpisodeSelector

import typer
import logging
from devgoldyutils import Colours

from . import ui, utils
from ..config import Config
from ..media import MetadataType
from ..logger import mov_cli_logger
from ..http_client import HTTPClient

__all__ = ("mov_cli",)

uwu_app = typer.Typer(pretty_exceptions_enable = False) # NOTE: goldy has an uwu complex.

def mov_cli(
    query: Optional[List[str]] = typer.Argument(None, help = "A film, tv show or anime you would like to Query."), 
    debug: Optional[bool] = typer.Option(None, help = "Enable extra logging details. Useful for bug reporting."), 
    player: Optional[str] = typer.Option(None, "--player", "-p", help = "Player you would like to stream with. E.g. mpv, vlc"), 
    scraper: Optional[str] = typer.Option(None, "--scraper", "-s", help = "Scraper you would like to scrape with. E.g. remote_stream, sflix"), 
    fzf: Optional[bool] = typer.Option(None, help = "Toggle fzf on/off for all user selection prompts."), 
    episode: Optional[str] = typer.Option(None, "--episode", "-ep", help = "Episode and season you wanna scrape. E.g {episode}:{season} like -> 26:3"), 

    version: bool = typer.Option(False, "--version", help = "Display what version mov-cli is currently on."), 
    edit: bool = typer.Option(False, "--edit", "-e", help = "Opens the mov-cli config with your respective editor."), 
):
    config = Config()

    config = utils.set_cli_config(
        config,
        debug = debug,
        player = player,
        scraper = scraper,
        fzf = fzf
    )

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    print(
        utils.welcome_msg(mov_cli_logger, True if len(query) == 0 else False, version)
    )

    mov_cli_logger.debug(f"Config -> {config.data}")

    if edit is True:
        utils.open_config_file(config)

    if len(query) > 0:
        query: str = " ".join(query)
        http_client = HTTPClient(config)

        scraper = config.default_scraper
        scraper_name, scraper_class_maybe = utils.get_scraper(scraper, config)

        if scraper_name is None:
            available_scrapers: List[str] = scraper_class_maybe

            mov_cli_logger.error(
                f"Could not find a scraper by the id '{scraper}'! Are you sure the plugin is installed and in your config?" \
                    f"\nAvailable Scrapers -> {available_scrapers}"
            )

            return False

        scraper_class: Scraper = scraper_class_maybe
        mov_cli_logger.info(f"Using '{Colours.BLUE.apply(scraper_name)}' scraper...")

        scraper: Scraper = scraper_class(config, http_client)

        mov_cli_logger.info(f"Searching for '{Colours.ORANGE.apply(query)}'...")

        choice = ui.prompt(
            "Choose Result", 
            choices = (choice for choice in scraper.search(query)), 
            display = lambda x: f"{Colours.CLAY if x.type == MetadataType.MOVIE else Colours.BLUE}{x.title}" \
                f"{Colours.RESET} ({x.year if x.year is not None else 'N/A'})", 
            config = config
        )

        if choice is None:
            mov_cli_logger.error("There was no results or you didn't select anything.")
            return False

        episode: EpisodeSelector = utils.handle_episode(
            episode = episode, 
            scraper = scraper, 
            choice = choice, 
            config = config
        )

        mov_cli_logger.info(f"Scrapping media for '{Colours.CLAY.apply(choice.title)}'...")
        media = scraper.scrape(choice, episode)

        popen = config.player.play(media)
        mov_cli_logger.debug(f"Streaming with this url -> '{media.url}'")

        popen.wait()

def app():
    uwu_app.command()(mov_cli)
    uwu_app() # Wait whaaaaa.