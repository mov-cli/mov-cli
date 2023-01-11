from pypresence import Presence
import time
from .dbs import get_imdb_title_and_img

try:
    dc = Presence("1008936657241767936")
    dc.connect()
except: 
    print("[X]: Error while connecting to Discord")

def update_presence(userinput):
        try:
            name, img = get_imdb_title_and_img(userinput)
        except:
            pass
        try:
            dc.update(state=f"Watching {name}", large_image=f"{img}", large_text=f"{name}", small_image="mov-cli",
                      small_text=f"{name}",
                      buttons=[{"label": "mov-cli", "url": "https://github.com/mov-cli/mov-cli"}],
                      start=time.time())
        except Exception as e:
            print(e)
            

def clear_presence():
    try:
        dc.clear()
    except:
        pass
