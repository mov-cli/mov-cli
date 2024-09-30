from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .platform import SUPPORTED_PLATFORMS

import os
from pathlib import Path

__all__ = (
    "get_appdata_directory", 
    "get_temp_directory", 
    "get_cache_directory"
)

LINUX_LIKE_FILE_STRUCTURE = ["Linux", "Android", "iOS", "FreeBSD"]

def get_appdata_directory(platform: SUPPORTED_PLATFORMS) -> Path:
    """Returns the path to the mov-cli appdata folder on multiple platforms."""
    appdata_dir = None

    if platform == "Windows":
        user_profile = Path(os.getenv("USERPROFILE"))
        appdata_dir = user_profile.joinpath("AppData", "Local")

    elif platform == "Darwin":
        user_profile = Path.home()
        appdata_dir = user_profile.joinpath("Library", "Application Support")

    elif platform in LINUX_LIKE_FILE_STRUCTURE:
        user_profile = Path(os.getenv("HOME"))
        appdata_dir = user_profile.joinpath(".config")

        appdata_dir.mkdir(exist_ok = True) # on android the .config file may not exist.

    appdata_dir = appdata_dir.joinpath("mov-cli")
    appdata_dir.mkdir(exist_ok = True)

    return appdata_dir

def get_temp_directory(platform: SUPPORTED_PLATFORMS) -> Path:
    """
    Returns the temporary directory where mov-cli can dump stuff. 
    Files stored here WILL get cleared / deleted automatically by the operating system.
    """
    temp_directory = None

    if platform == "Windows":
        temp_directory = Path(os.getenv("TEMP"))

    elif platform == "Darwin": # NOTE: Path maybe incorrect, please report failures!
        temp_directory = Path(os.getenv("TMPDIR"))

    elif platform == "Linux" or platform == "iOS" or platform == "FreeBSD":
        linux_temp_dir = os.getenv("TMPDIR") # Respect the TMPDIR environment variable on Linux: https://unix.stackexchange.com/a/362107

        if linux_temp_dir is None:
            linux_temp_dir = "/tmp"

        temp_directory = Path(linux_temp_dir)

    elif platform == "Android":
        temp_directory = Path(f"{os.getenv('PREFIX')}/tmp")

    temp_directory = temp_directory.joinpath("mov-cli-temp")
    temp_directory.mkdir(exist_ok = True)

    return temp_directory

def get_cache_directory(platform: SUPPORTED_PLATFORMS) -> Path:
    """
    Returns the cache directory where mov-cli can dump longer lived cache.
    """
    cache_directory = None

    if platform == "Windows":
        cache_directory = Path(os.getenv("LOCALAPPDATA"))

    elif platform == "Darwin": # NOTE: Path maybe incorrect
        user_profile = Path.home()
        cache_directory = user_profile.joinpath("Library", "Caches")

    elif platform in LINUX_LIKE_FILE_STRUCTURE:
        user_profile = Path(os.getenv("HOME"))
        cache_directory = user_profile.joinpath(".cache")

        cache_directory.mkdir(exist_ok = True) # on android the .cache file may not exist.

    cache_directory = cache_directory.joinpath("mov-cli")
    cache_directory.mkdir(exist_ok = True)

    return cache_directory