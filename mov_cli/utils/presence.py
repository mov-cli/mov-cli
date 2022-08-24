from pypresence import Presence
import re
import time
from .config import config
from colorama import Fore, Style
import imdb

try:
    dc = Presence("1008936657241767936")
    dc.connect()
except: 
    print("[X]: Error while connecting to Discord")

def update_presence(userinput, season=None, episode=None):
    if config.getpresence() is True:
        name = movieinfo(userinput, season, episode)
        try:
            dc.update(state=f"Watching {name}", large_image="logo", large_text="mov-cli", buttons=[{"label": "mov-cli", "url": "https://mov-cli.github.io/mov-cli"}], start=time.time())
        except:
            pass
    else:
        pass

def movieinfo(userinput, season=None, episode=None):
    userinput = re.sub(r"-+", " ", userinput)
    
    db = imdb.IMDb()
    search = db.search_movie(userinput)

    id = search[0].getID()

    movie = db.get_movie(id)

    title = movie["title"]
    
    if season is None:
        return title
    else:
        return f"{title} - S{season} EP{episode}"

def clear_presence():
    if config.getpresence() is True:
        try:
            dc.clear()
        except:
            pass
    else:
        pass
