import re
import subprocess

import mov_cli.__main__ as movcli
from fzf import fzf_prompt

from .httpclient import HttpClient
from .lang import getlang, setlang
from .player import PlayerNotFound
from ..players.player import ply
from ..extractors.doodstream import dood
from ..extractors.tukipasti import tukipasti

# import shlex
# required for development


class WebScraper:
    def __init__(self, base_url: str) -> None:
        self.client = HttpClient()
        self.base_url = base_url
        (self.title, self.url, self.aid, self.mv_tv) = (0, 1, 2, 3)
        self.translated = getlang()
        (
            self.task,
            self.exit,
            self.searcha,
            self.download,
            self.sprovider,
            self.dshow,
            self.dseason,
            self.tse,
            self.tep,
            self.change,
        ) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.scraper = self.parser()
        self.dseasonp = False
        self.dshowp = False
        pass

    def parser(self):
        try:
            import lxml

            return "lxml"
        except ModuleNotFoundError:
            return "html.parser"

    @staticmethod
    def parse(txt: str) -> str:
        return re.sub(r"\W+", "-", txt.lower())

    def dl(
        self,
        url: str,
        name: str,
        subtitle: str = None,
        season="",
        episode=None,
        referrer: str = None,
    ):
        name = self.parse(name)
        fixname = re.sub(r"-+ +", " ", name)
        if episode and season:
            fixname = f"{fixname} S{season}E{episode}"
        
        if episode:
            fixname = f"{fixname} E{episode}"

        if referrer:
            referrer = referrer
        else:
            referrer = self.base_url
        # args = shlex.split(f 'ffmpeg -i "{url}" -c copy {self.parse(name)}.mp4')
        args = [
            "ffmpeg",
            "-n",
            "-thread_queue_size",
            "4096",
            "-headers",
            f"Referer: {referrer}",
            "-i",
            f"{url}",
            "-c",
            "copy",
            f"{fixname}.mp4",
        ]

        if subtitle:
            args.extend(["-vf", f"subtitle={subtitle}", f"{fixname}.mp4"])
        ffmpeg_process = subprocess.Popen(args)
        ffmpeg_process.wait()
        return

    def play(self, url: str, name: str, referrer=None):
        if referrer is None:
            referrer = self.base_url
        try:
            ply_process = ply(self).play(url, referrer, name)
            ply_process.wait()
        except PlayerNotFound as e:
            txt = f"[!] Could not play: Correct Player for your OS was not found | {e}"
            # logging.log(logging.ERROR, txt)
            print(txt)  # TODO implement logging to a file
            exit(1)

    def search(self, q: str = None) -> str:
        pass
        # return NotImplementedError()

    def results(self, data: str) -> list:
        pass
        # return NotImplementedError()

    def TV_PandDP(self, t: list, state: str):
        pass

    def MOV_PandDP(self, m: list, state: str):
        pass

    def SandR(self, q: str = None):
        return self.results(self.search(q))

    def display(self, q: str = None, result_no: int = None):
        result = self.SandR(q)
        r = []
        for ix, vl in enumerate(result):
            r.append(f"[{ix + 1}] {vl[self.title]} {vl[self.mv_tv]}")
        r.extend(
            [
                f"[q] {self.translated[self.exit]}",
                f"[s] {self.translated[self.searcha]}",
                f"[d] {self.translated[self.download]}",
                f"[p] {self.translated[self.sprovider]}",
                f"[c] {self.translated[self.change]}",
            ]
        )
        r = r[::-1]
        choice = ""
        while choice not in range(len(result) + 1):
            choice = (
                re.findall(r"\[(.*?)\]", fzf_prompt(r))[0]
                if not result_no
                else result_no
            )
            if choice == "q":
                exit()
            elif choice == "s":
                return self.redo()
            elif choice == "p":
                return movcli.movcli()
            elif choice == "c":
                setlang()
                return movcli.movcli()
            elif choice == "d":
                try:
                    modes = [f"[d] {self.translated[self.download]}"]
                    if self.dshowp and self.dseasonp:
                        modes.extend(
                            [
                                f"[s] {self.translated[self.dshow]}",
                                f"[e] {self.translated[self.dseason]}",
                            ]
                        )
                    elif self.dseasonp is True:
                        modes.append(f"[e] {self.translated[self.dseason]}")
                    elif self.dshowp is True:
                        modes.append(f"[s] {self.translated[self.dshow]}")
                    else:
                        pass
                    modes = modes[::-1]
                    mode = fzf_prompt(modes, header="Select a mode:")[1]
                    choice = (
                        re.findall(r"\[(.*?)\]", fzf_prompt(r))[0]
                        if not result_no
                        else result_no
                    )
                    mov_or_tv = result[int(choice) - 1]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, mode)
                    else:
                        if mode == "e" or mode == "s":
                            print(
                                "Those options are not unavailable for movies. Using d."
                            )
                            mode = "d"
                        self.MOV_PandDP(mov_or_tv, mode)
                except ValueError as e:
                    print(
                        "[!]  Invalid Choice Entered! | ",
                        str(e),
                    )
                    exit(1)
                except IndexError as e:
                    print(
                        "[!]  This Episode is coming soon! | ",
                        str(e),
                    )
                    exit(2)
            else:
                mov_or_tv = result[int(choice) - 1]
                if mov_or_tv[self.mv_tv] == "TV":
                    self.TV_PandDP(mov_or_tv, "p")
                else:
                    self.MOV_PandDP(mov_or_tv, "p")

    def tuki(self, html: str):
        return tukipasti(html)

    def doodstream(self, url: str):
        return dood(url)

    def redo(self, search: str = None, result: int = None):
        return self.display(search, result)

    def askseason(self, seasons: int):
        texts = []
        for i in range(seasons):
            texts.append(f"{self.translated[self.tse]} {i+1}")
        choice = fzf_prompt(texts).split(" ")[-1]
        return choice

    def askepisode(self, episodes: int):
        texts = []
        for i in range(episodes):
            texts.append(f"{self.translated[self.tep]} {i+1}")
        choice = fzf_prompt(texts).split(" ")[-1]
        return choice
