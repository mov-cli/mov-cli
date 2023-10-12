from os import environ, mkdir, path
from getpass import getuser
from .player import Player


def home():
    plt = Player().os
    if plt == "Windows":
        home = path.expanduser('~')
        return f"{home}/AppData/Roaming/mov-cli"
    elif plt == "Linux":
        return f"/home/{getuser()}/.config/mov-cli"
    elif plt == "Android":
        return f"/data/data/com.termux/files/home"
    elif plt == "iOS":
        return "/root/mov-cli_config"
    elif plt == "Darwin":
        return f"/Users/{getuser()}/Library/Application Support/mov-cli"

def firstStart():
    print(home())
    if not path.exists(home()):
        mkdir(home())


class RestartNeeded(Exception):
    """Raise when mov-cli is needed to restart."""

    def __init__(self) -> None:
        super().__init__(f"Please restart mov-cli.")


class LanguageNotAOption(Exception):
    """Raise when Language is not a Option."""

    def __init__(self, lang) -> None:
        super().__init__(
            f"This language '{lang}' is not available Option in the Language's tab. \r\nPlease delete lang.mov-cli in {home()}"
        )


class SelectedNotAvailable(Exception):
    """Raise when the selected item is not Available or was removed."""

    def __init__(self) -> None:
        super().__init__("Not available or it was removed")


class NoSupportedProvider(Exception):
    """Raise when no supported provider was found."""

    def __init__(self) -> None:
        super().__init__("No supported provider was found")
