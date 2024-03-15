"""
A script we use to test subtitles in development.

You must run it like so in the **root directory** -> python scripts/test_subtitles.py
"""
import sys
sys.path.insert(0, ".")

from mov_cli.subtitles import Subtitles
from mov_cli.utils import EpisodeSelector
from mov_cli import Config, mov_cli_logger

if __name__ == "__main__":
    """
    Add this to your config to test.

    [mov-cli.subtitles.open_subtitles]
    key = "{your_key}"

    """

    config = Config()

    if config.open_subtitles_key is None:
        mov_cli_logger.error("You don't have a key specified for open subtitles! Get one at ")
        exit()

    subs = Subtitles(config.open_subtitles_key)

    print(subs.get_subtitles("community", EpisodeSelector(4, 1)))