import logging
from devgoldyutils import add_custom_handler

__all__ = ("mov_cli_logger",)

mov_cli_logger = add_custom_handler(
    logger = logging.getLogger("mov_cli"),
    level = logging.WARNING
)
