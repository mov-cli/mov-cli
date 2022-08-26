from pypresence import Presence
import time
from .config import config
from .dbs import get_imdb_title

try:
    dc = Presence("1008936657241767936")
    dc.connect()
except: 
    print("[X]: Error while connecting to Discord")

def update_presence(userinput, season=None, episode=None):
    if config.getpresence() is True:
        name = get_imdb_title(userinput)
        if season is None:
            pass
        else:
            name = f"{name} - S {season} EP {episode}"
        try:
            dc.update(state=f"Watching {name}", large_image="logo", large_text="mov-cli", buttons=[{"label": "mov-cli", "url": "https://mov-cli.github.io/mov-cli"}, {"label": "GitHub", "url": "https://github.com/mov-cli/mov-cli"}], start=time.time())
        except:
            pass
    else:
        pass

def clear_presence():
    if config.getpresence() is True:
        try:
            dc.clear()
        except:
            pass
    else:
        pass
