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
        super().__init__(
            f"Please restart mov-cli."
        )

class LanguageNotAOption(Exception):
    """Raise when Language is not a Option."""

    def __init__(self, lang) -> None:
        super().__init__(
            f"This language '{lang}' is not available Option in the Language's tab. \r\nPlease delete .mov_cli_lang in your home directory."
        )