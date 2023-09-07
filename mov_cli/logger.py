import logging
from devgoldyutils import add_custom_handler, Colours

__all__ = ("mov_cli_logger",)

mov_cli_logger = add_custom_handler(
    logger = logging.getLogger(Colours.WHITE.apply("mov_cli")), 
    level = logging.INFO
)