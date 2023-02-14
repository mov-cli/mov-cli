import httpx
from mov_cli.__version__ import __core__ as local

def check():
    github = httpx.get("https://raw.githubusercontent.com/mov-cli/mov-cli/v3/mov_cli/__version__.py").text.split('"')[1]
    if github > local:
        return True
    else:
        return False