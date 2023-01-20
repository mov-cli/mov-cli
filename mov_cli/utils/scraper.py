import logging
import os
#import platform
import re
import subprocess
import sys
import mov_cli.__main__ as movcli
# import shlex
# required for development
from colorama import Fore, Style
from .httpclient import HttpClient

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
    def blue(txt: str) -> str:
        return f"{Fore.BLUE}{txt}{Style.RESET_ALL}"

    @staticmethod
    def yellow(txt: str) -> str:
        return f"{Fore.YELLOW}{txt}{Style.RESET_ALL}"

    @staticmethod
    def red(txt: str) -> str:
        return f"{Fore.RED}{txt}{Style.RESET_ALL}"

    @staticmethod
    def lmagenta(txt: str) -> str:
        return f"{Fore.LIGHTMAGENTA_EX}{txt}{Style.RESET_ALL}"
    
    @staticmethod
    def cyan(txt: str) -> str:
        return f"{Fore.CYAN}{txt}{Style.RESET_ALL}"

    @staticmethod
    def green(txt: str) -> str:
        return f"{Fore.GREEN}{txt}{Style.RESET_ALL}"

    @staticmethod
    def parse(txt: str) -> str:
        return re.sub(r"\W+", "-", txt.lower())

    def dl(
        self, url: str, name: str, subtitle: str = None, season = None, episode = None
    ):
        name = self.parse(name)
        fixname = re.sub(r"-+", " ", name)
        fixname = f"{fixname}S{season}E{episode}"

        # args = shlex.split(f 'ffmpeg -i "{url}" -c copy {self.parse(name)}.mp4')
        args = [
        'ffmpeg',
        '-n', 
        '-thread_queue_size',
        '4096',
        '-err_detect',
        'ignore_err',
        '-i', 
        f'{url}',
        "-user_agent",
        '"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"',
        '-c', 
        'copy',
        '-preset',
        'ultrafast',
        f'{fixname}.mp4'
        ]

        if subtitle:
            # args.extend(f'-vf subtitle="{subtitle}" {self.parse(name)}.mp4')
            args.extend(
                ["-vf", f"subtitle={subtitle}", f"{fixname}.mp4"]
            )
        ffmpeg_process = subprocess.Popen(args)
        ffmpeg_process.wait()
        
        return print(f"Downloaded at {os.getcwd()}")

    def play(self, url: str, name: str):
        try:
            try:
                args = [
                    "mpv",
                    f"--referrer={self.base_url}",
                    f"{url}",
                    f"--force-media-title=mov-cli:{name}",
                    "--no-terminal",
                ]
                mpv_process = subprocess.Popen(
                    args  # stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
                )
                mpv_process.wait()
            except ModuleNotFoundError:  # why do you even exist if you don't have MPV installed? WHY?
                args = [
                    "vlc",
                    f"--http-referrer={self.base_url}",
                    f"{url}",
                    f"--meta-title=mov-cli{name}",
                    "--no-terminal",
                ]
                vlc_process = subprocess.Popen(
                    args  # stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
                )
                vlc_process.wait()
        except Exception as e:
            txt = f"{self.red('[!]')} Could not play {name}: MPV or VLC not found | {e}"
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
        for ix, vl in enumerate(result):
            print(  
                self.green(f"[{ix + 1}] {vl[self.title]} {vl[self.mv_tv]}"), end="\n\n"
            )
        print(self.red("[q] Exit!"), end="\n\n")
        print(self.yellow("[s] Search Again!"), end="\n\n")
        print(self.cyan("[d] Download!"), end="\n\n")
        print(self.green("[p] Switch Provider!"), end="\n\n")
        print(self.green("[sd] Download Whole Show!"), end="\n\n")
        choice = ""
        while choice not in range(len(result) + 1):
            choice = (
                input(self.blue("Enter your choice: ")) if not result_no else result_no
            )
            if choice == "q":
                sys.exit()
            elif choice == "s":
                return self.redo()
            elif choice == "p":
                return movcli.movcli()
            elif choice == "d":
                try:
                    mov_or_tv = result[
                        int(
                            input(
                                self.yellow(
                                    "[!] Please enter the number of the movie you want to download: "
                                )
                            )
                        )
                        - 1
                    ]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, "d")
                    else:
                        self.MOV_PandDP(mov_or_tv, "d")
                except ValueError as e:
                    print(
                        self.red(f"[!]  Invalid Choice Entered! | "),
                        self.lmagenta(str(e)),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        self.red(f"[!]  This Episode is coming soon! | "),
                        self.lmagenta(str(e)),
                    )
                    sys.exit(2)
            elif choice == "sd":
                try:
                    mov_or_tv = result[
                        int(
                            input(
                                self.yellow(
                                    "[!] Please enter the number of the movie you want to download: "
                                )
                            )
                        )
                        - 1
                    ]
                    if mov_or_tv[self.mv_tv] == "TV":
                        self.TV_PandDP(mov_or_tv, "sd")
                    else:
                        self.MOV_PandDP(mov_or_tv, "sd")
                except ValueError as e:
                    print(
                        self.red(f"[!]  Invalid Choice Entered! | "),
                        self.lmagenta(str(e)),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        self.red(f"[!]  This Episode is coming soon! | "),
                        self.lmagenta(str(e)),
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
