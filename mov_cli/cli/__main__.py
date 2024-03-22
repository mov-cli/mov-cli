from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..scraper import Scraper
    from ..utils import EpisodeSelector

import typer
import logging
from devgoldyutils import Colours

from . import ui, utils
from .scraper import select_scraper
from .auto_select import auto_select_choice

from ..config import Config
from ..media import MetadataType
from ..logger import mov_cli_logger
from ..http_client import HTTPClient
from ..download import Download

__all__ = ("mov_cli",)

uwu_app = typer.Typer(pretty_exceptions_enable = False) # NOTE: goldy has an uwu complex.

def mov_cli(
    query: Optional[List[str]] = typer.Argument(None, help = "A film, tv show or anime you would like to Query."), 
    debug: Optional[bool] = typer.Option(None, help = "Enable extra logging details. Useful for bug reporting."), 
    player: Optional[str] = typer.Option(None, "--player", "-p", help = "Player you would like to stream with. E.g. mpv, vlc"), 
    scraper: Optional[str] = typer.Option(None, "--scraper", "-s", help = "Scraper you would like to scrape with. E.g. remote_stream, sflix"), 
    fzf: Optional[bool] = typer.Option(None, help = "Toggle fzf on/off for all user selection prompts."), 
    episode: Optional[str] = typer.Option(None, "--episode", "-ep", help = "Episode and season you wanna scrape. E.g. {episode}:{season} like -> 26:3"), 
    auto_select: Optional[int] = typer.Option(None, "--choice", "-c", help = "Auto select the search results. E.g. Setting it to 1 with query 'nyan cat' will pick " \
        "the first nyan cat video to show up in search results."
    ), 

    version: bool = typer.Option(False, "--version", help = "Display what version mov-cli is currently on."), 
    edit: bool = typer.Option(False, "--edit", "-e", help = "Opens the mov-cli config with your respective editor."), 
    download: bool = typer.Option(False, "--download", "-d", help = "Downloads the media instead of playing.")
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

        chosen_scraper = select_scraper(config.plugins, config.fzf_enabled, config.default_scraper)

        if chosen_scraper is None:
            mov_cli_logger.error(
                "You must choose a scraper to scrape with! " \
                    "You can set a default scraper with the default key in config.toml."
            )
            return False

        scraper_name, scraper_class = chosen_scraper

        mov_cli_logger.info(f"Using '{Colours.BLUE.apply(scraper_name)}' scraper...")
        scraper: Scraper = scraper_class(config, http_client)

        mov_cli_logger.info(f"Searching for '{Colours.ORANGE.apply(query)}'...")

        choice = None

        if auto_select is not None:
            choice = auto_select_choice((choice for choice in scraper.search(query)), auto_select)
        else:
            choice = ui.prompt(
                "Choose Result", 
                choices = (choice for choice in scraper.search(query)), 
                display = lambda x: f"{Colours.CLAY if x.type == MetadataType.MOVIE else Colours.BLUE}{x.title}" \
                    f"{Colours.RESET} ({x.year if x.year is not None else 'N/A'})", 
                fzf_enabled = config.fzf_enabled
            )

        if choice is None:
            mov_cli_logger.error("There was no results or you didn't select anything.")
            return False

        episode: Optional[EpisodeSelector] = utils.handle_episode(
            episode_string = episode, 
            scraper = scraper, 
            choice = choice, 
            fzf_enabled = config.fzf_enabled
        )

        if episode is None:
            mov_cli_logger.error("You didn't select a season/episode.")
            return False

        mov_cli_logger.info(f"Scrapping media for '{Colours.CLAY.apply(choice.title)}'...")
        media = scraper.scrape(choice, episode)

        if download:
            dl = Download(config)
            mov_cli_logger.debug(f"Downloading from this url -> '{media.url}'")

            popen = dl.download(media)
            popen.wait()

        else:
            platform = utils.what_platform()

            popen = config.player(platform = platform).play(media)

            if popen is None:
                mov_cli_logger.error(
                    f"The player '{config.player.__class__.__name__.lower()}' is not supported on this platform ({platform}). " \
                    "We recommend VLC for iOS and MPV for every other platform."
                )

                return False

            mov_cli_logger.debug(f"Streaming with this url -> '{media.url}'")

            if not platform == "iOS":
                popen.wait()

def app():
    uwu_app.command()(mov_cli)
    uwu_app() # Wait whaaaaa.