from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    ...

import typer
import logging
from devgoldyutils import Colours

from .play import play
from .search import search
from .episode import handle_episode
from .scraper import select_scraper, use_scraper, scrape
from .configuration import open_config_file, set_cli_config
from .utils import welcome_msg, steal_scraper_args

from ..config import Config
from ..download import Download
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
    episode: Optional[str] = typer.Option(None, "--episode", "-ep", help = "Episode and season you wanna scrape. E.g. {episode}:{season} like -> 26:3"), 
    auto_select: Optional[int] = typer.Option(None, "--choice", "-c", help = "Auto select the search results. E.g. Setting it to 1 with query 'nyan cat' will pick " \
        "the first nyan cat video to show up in search results."
    ), 

    version: bool = typer.Option(False, "--version", help = "Display what version mov-cli is currently on."), 
    edit: bool = typer.Option(False, "--edit", "-e", help = "Opens the mov-cli config with your respective editor."), 
    download: bool = typer.Option(False, "--download", "-d", help = "Downloads the media instead of playing.")
):
    config = Config()

    config = set_cli_config(
        config,
        debug = debug,
        player = player,
        scraper = scraper,
        fzf = fzf
    )

    if config.debug:
        mov_cli_logger.setLevel(logging.DEBUG)

    print(
        welcome_msg(True if query is None else False, version)
    )

    mov_cli_logger.debug(f"Config -> {config.data}")

    if edit is True:
        open_config_file(config)
        return None

    if query is not None:
        scrape_args = steal_scraper_args(query) 
        # This allows passing arguments to scrapers like this: 
        # https://github.com/mov-cli/mov-cli-youtube/commit/b538d82745a743cd74a02530d6a3d476cd60b808#diff-4e5b064838aa74a5375265f4dfbd94024b655ee24a191290aacd3673abed921a

        query: str = " ".join(query)

        http_client = HTTPClient(config)

        selected_scraper = select_scraper(config.plugins, config.fzf_enabled, config.default_scraper)

        if selected_scraper is None:
            mov_cli_logger.error(
                "You must choose a scraper to scrape with! " \
                    "You can set a default scraper with the default key in config.toml."
            )
            return False

        chosen_scraper = use_scraper(selected_scraper, config, http_client)

        choice = search(query, auto_select, chosen_scraper, config.fzf_enabled)

        if choice is None:
            mov_cli_logger.error("There was no results or you didn't select anything.")
            return False

        chosen_episode = handle_episode(
            episode_string = episode, 
            scraper = chosen_scraper, 
            choice = choice, 
            fzf_enabled = config.fzf_enabled
        )

        if chosen_episode is None:
            mov_cli_logger.error("You didn't select a season/episode.")
            return False

        media = scrape(choice, chosen_episode, chosen_scraper, **scrape_args)

        if download:
            dl = Download(config)
            mov_cli_logger.debug(f"Downloading from this url -> '{media.url}'")

            popen = dl.download(media)
            popen.wait()

        else:
            option = play(media, choice, chosen_scraper, chosen_episode, config, scrape_args)

            if option == "search":
                query = input(Colours.BLUE.apply("  Enter Query: "))

                mov_cli(
                    query = [query], 
                    debug = debug, 
                    player = player, 
                    scraper = scraper, 
                    fzf = fzf,
                    episode = None,
                    auto_select = None,

                    version = False,
                    edit = False,
                    download = False
                )

def app():
    uwu_app.command()(mov_cli)
    uwu_app() # Wait whaaaaa.