from .cli import *
from .media import *
from .cache import *
from .config import *
from .scraper import *
from .download import *

import warnings

warnings.warn(
    "The ability to import objects directly from the mov-cli library like this: " \
        "'from mov-cli import Scraper' WILL BE REMOVED IN v4.6!!! CHANGE YOUR IMPORTS NOW!\n" \
            "E.g. Instead of 'from mov-cli import Scraper' do 'from mov-cli.scraper import Scraper'!",
    category = DeprecationWarning,
    stacklevel = 3
)

__version__ = "4.5alpha1"
