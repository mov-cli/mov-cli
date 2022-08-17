from pypresence import Presence
import re
import time
from .config import config

dc = Presence("1008936657241767936")
dc.connect()

def update_presence(name):
    if config.getpresence() is True:
        name = re.sub(r"-+", " ", name)
        name = re.sub(r"_+", " ", name)
        dc.update(state=f"Watching {name}", large_image="logo", large_text="mov-cli", buttons=[{"label": "mov-cli", "url": "https://mov-cli.github.io/mov-cli"}], start=time.time())
    else:
        pass
def clear_presence():
    dc.clear()

