import logging
import os
#import platform
import re
import subprocess
import sys
import mov_cli.__main__ as movcli
# import shlex
# required for development

from .httpclient import HttpClient
from fzf import fzf_prompt
from platform import system

from .player import PlayerNotFound
from ..players.mpv import Mpv
from ..players.vlc import Vlc

# Not needed
# def determine_path() -> str:
#    plt = platform.system()
#    if plt == "Windows":
#        return f"C://Users//{os.getenv('username')}//Downloads"
#    elif (plt == "Linux") or (plt == "Darwin"):
#        return f"/home/{os.getlogin()}/Downloads"
#    else:
#        print("Please open an issue for your os")
#        sys.exit(-2)


class WebScraper:
    def __init__(self, base_url: str) -> None:
        self.client = HttpClient()
        self.base_url = base_url
        self.title, self.url, self.aid, self.mv_tv = 0, 1, 2, 3
        pass

    @staticmethod
    def parse(txt: str) -> str:
        return re.sub(r"\W+", "-", txt.lower())

    def dl(
        self, url: str, name: str, subtitle: str = None, season = "", episode = None, referrer: str = None
    ):
        name = self.parse(name)
        fixname = re.sub(r"-+", " ", name)
        if episode:
            fixname = f"{fixname} S{season}E{episode}"
        
        if referrer:
            referrer = referrer
        else:
            referrer = self.base_url
        # args = shlex.split(f 'ffmpeg -i "{url}" -c copy {self.parse(name)}.mp4')
        args = [
        'ffmpeg',
        '-n',
        f'-headers',
        f'Referer: {referrer}',
        '-i', 
        f'{url}',
        '-c', 
        'copy',
        f'{fixname}.mp4'
        ]
        print(str(args))

        if subtitle:
            # args.extend(f'-vf subtitle="{subtitle}" {self.parse(name)}.mp4')
            args.extend(
                ["-vf", f"subtitle={subtitle}", f"{fixname}.mp4"]
            )
        ffmpeg_process = subprocess.Popen(args)
        ffmpeg_process.wait()
        
        return print(f"Downloaded at {os.getcwd()}")

    def play(self, url: str, name: str, referrer = None):
        if referrer is None: referrer == self.base_url
        try:
            try:
                mpv_process = Mpv(self).play(url, referrer, name)
                mpv_process.wait()
            except PlayerNotFound:  # why do you even exist if you don't have MPV installed? WHY?
                vlc_process = Vlc(self).play(url, referrer, name)
                vlc_process.wait()
        except Exception as e:
            txt = f"{self.red('[!]')} Could not play {name}: MPV not found | {e}"
            logging.log(logging.ERROR, txt)
            # print(txt)  # TODO implement logging to a file
            sys.exit(1)

    def search(self, q: str = None) -> str:
        pass
        # return NotImplementedError()

    def results(self, data: str) -> list:
        pass
        # return NotImplementedError()

    def TV_PandDP(self, t: list, state: str = "d" or "p"):
        pass

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        pass

    def SandR(self, q: str = None):
        return self.results(self.search(q))

    def display(self, q: str = None, result_no: int = None):
        result = self.SandR(q)
        r = [] 
        for ix, vl in enumerate(result):
            r.append(f"[{ix + 1}] {vl[self.title]} {vl[self.mv_tv]}")
        r.extend(["","[q] Exit!","[s] Search Again!","[d] Download!","[p] Switch Provider!","[sd] Download Whole Show!","[ds] Download Season!"])
        r = r[::-1]
        choice = ""
        while choice not in range(len(result) + 1):
            pre = fzf_prompt(r)
            choice = (
                re.findall(r"\[(.*?)\]", pre)[0] if not result_no else result_no
            )
            if choice == "q":
                sys.exit()
            elif choice == "s":
                return self.redo()
            elif choice == "p":
                return movcli.movcli()
            elif choice == "d":
                try:
                    pre = fzf_prompt(r)
                    choice = re.findall(r"\[(.*?)\]", pre)[0] if not result_no else result_no
                    mov_or_tv = result[int(choice) - 1]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, "d")
                    else:
                        self.MOV_PandDP(mov_or_tv, "d")
                except ValueError as e:
                    print(
                        f"[!]  Invalid Choice Entered! | ",
                        str(e),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        "[!]  This Episode is coming soon! | ",
                        str(e),
                    )
                    sys.exit(2)
            elif choice == "sd":
                try:
                    pre = fzf_prompt(r)
                    choice = re.findall(r"\[(.*?)\]", pre)[0] if not result_no else result_no
                    mov_or_tv = result[int(choice) - 1]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, "sd")
                    else:
                        print("You selected a Movie")
                        exit(0)
                except ValueError as e:
                    print(
                        f"[!]  Invalid Choice Entered! | ",
                        str(e),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        "[!]  This Episode is coming soon! | ",
                        str(e),
                    )
                    sys.exit(2)
            elif choice == "ds":
                try:
                    pre = fzf_prompt(r)
                    choice = re.findall(r"\[(.*?)\]", pre)[0] if not result_no else result_no
                    mov_or_tv = result[int(choice) - 1]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, "ds")
                    else:
                        print("You selected a Movie")
                        exit(0)
                except ValueError as e:
                    print(
                        f"[!]  Invalid Choice Entered! | ",
                        str(e),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        "[!]  This Episode is coming soon! | ",
                        str(e),
                    )
                    sys.exit(2)
            else:
                mov_or_tv = result[int(choice) - 1]
                if mov_or_tv[self.mv_tv] == "TV":
                    self.TV_PandDP(mov_or_tv, "p")
                else:
                    self.MOV_PandDP(mov_or_tv, "p")

    def redo(self, search: str = None, result: int = None):
        print(result)
        return self.display(search, result)
    
    def askseason(self, seasons: int):
        texts = []
        for i in range(seasons):
            texts.append(f"Season {i+1}")
        choice = fzf_prompt(texts).split(" ")[-1]
        return choice
    
    def askepisode(self, episodes: int):
        texts = []
        for i in range(episodes):
            texts.append(f"Episode {i+1}")
        choice = fzf_prompt(texts).split(" ")[-1]
        return choice
