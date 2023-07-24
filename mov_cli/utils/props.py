from platform import system as pf
from os import environ
from getpass import getuser


def home():
    plt = pf()
    if plt == "Windows":
        username = environ["username"]
        return f"C:/Users/{username}/"
    elif (plt == "Linux") or (plt == "Darwin"):
        return f"/home/{getuser()}/"


class RestartNeeded(Exception):
    """Raise when mov-cli is needed to restart."""

    def __init__(self) -> None:
        super().__init__(f"Please restart mov-cli.")


class LanguageNotAOption(Exception):
    """Raise when Language is not a Option."""

    def __init__(self, lang) -> None:
        super().__init__(
            f"This language '{lang}' is not available Option in the Language's tab. \r\nPlease delete provider.mov-cli in your home directory."
        )


class SelectedNotAvailable(Exception):
    """Raise when the selected item is not Available or was removed."""

    def __init__(self) -> None:
        super().__init__("Not available or it was removed")


class NoSupportedProvider(Exception):
    """Raise when no supported provider was found."""

    def __init__(self) -> None:
        super().__init__("No supported provider was found")
