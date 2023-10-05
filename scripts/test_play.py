import sys
sys.path.insert(0, ".")

import logging
from devgoldyutils import pprint

from mov_cli.players import MPV
from mov_cli.config import Config
from mov_cli.scrapers import Gogoanime, RemoteStream, Sflix, Turkish123, SolarMovies
from mov_cli.logger import mov_cli_logger
from mov_cli.http_client import HTTPClient

mov_cli_logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    config = Config()
    remote_stream = Sflix(config, HTTPClient(config))

    results = remote_stream.search(" ")
    pprint(results)

    movie = remote_stream.scrape(results[0])

    MPV(config).play(movie)