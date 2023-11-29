import sys
sys.path.insert(0, ".")

import logging

from mov_cli.players import MPV
from mov_cli.config import Config
from mov_cli.scrapers import Gogoanime, RemoteStream, Sflix, Turkish123, SolarMovies
from mov_cli.logger import mov_cli_logger
from mov_cli.http_client import HTTPClient

mov_cli_logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    config = Config()
    remote_stream = RemoteStream(config, HTTPClient(config))

    results = remote_stream.search("Breaking Bad")

    print(results)

    print(results[-1].get_extra())

    movie = remote_stream.scrape(results[-1])

    MPV(config).play(movie)