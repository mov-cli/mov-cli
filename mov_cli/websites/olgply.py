import sys

# import httpx

sys.path.append("..")

from ..utils.scraper import WebScraper
from ..utils.dbs import *


class OlgPly(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    # def search(self, query=None):
    #    query = input(self.blue("[!] Please Enter the name of the Movie: ")) if query is None else query
    #    return self.client.get(f'{self.base_url}/search?q={query}').text

    def search(self, q: str = None) -> list:
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return get_tmdb_id(q)

    # !returns title, url , id, mv_tv

    def cdn_url(self, name):
        imdb_id = get_imdb_id(name)
        req = httpx.get(
            f"https://olgply.com/api/?imdb={imdb_id}",
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux "
                              "x86_64; rv:100.0) "
                              "Gecko/20100101 "
                              "Firefox/100.0"
            },
        ).text
        url = re.findall(r"https?:[a-zA-Z\d.+-/#~]+\.mp4", req)
        print(url)
        return url[0], name

    def cdn_url_ws(self, season, episode, name):
        imdb_id = get_imdb_id(name)
        print(
            f"https://olgply.com/api/?imdb={imdb_id}&season={season}&episode={episode}"
        )
        req = httpx.get(
            f"https://olgply.com/api/?imdb={imdb_id}&season={season}&episode={episode}",
            headers={
                "User-Agent": "Mozilla"
                              "/5.0 ("
                              "X11; "
                              "Linux "
                              "x86_64; "
                              "rv:100"
                              ".0) "
                              "Gecko"
                              "/20100101 Firefox/100.0"
            },
        ).text
        url = re.findall(r"https?:[a-zA-Z\d_.+-/#~]+\.mp4", req)
        print(url)
        return url[0], name

    def ask(self, tmdb_id, name):
        seasons = get_season_seasons(tmdb_id, name)
        season = input(
            self.lmagenta(f"Please input the season number(total seasons:{seasons}): ")
        )
        episodes = get_season_episodes(tmdb_id, name, season)
        episode = input(
            self.lmagenta(
                f"Please input the episode number(total episodes:{episodes}): "
            )
        )
        return self.cdn_url_ws(season, episode, f"{name}_S{season}_E{episode}")

    def display(self, result):
        for ix, vl in enumerate(result):
            print(self.green(f"[{ix + 1}] {vl[0]} {vl[-1]}"), end="\n\n")
        print(self.red("[q] Exit!"), end="\n\n")
        print(self.yellow("[s] Search Again!"), end="\n\n")
        print(self.cyan("[d] Download!"), end="\n\n")
        choice = ""
        while choice not in range(len(result) + 1):
            choice = input(self.blue("Enter your choice: "))
            if choice == "q":
                sys.exit()
            elif choice == "s":
                return self.redo()
            elif choice == "d":
                try:
                    mov = result[
                        int(
                            input(
                                self.yellow(
                                    "[!] Please enter the number of the movie you want to download: "
                                )
                            )
                        )
                        - 1
                        ]
                    name = mov[0]
                    if mov[-1] == "TV":
                        cdnurl, name = self.ask(mov[2], name)
                        self.dl(cdnurl, name)
                    else:
                        cdn, name = self.cdn_url(name)
                        self.dl(cdn, name)
                except ValueError as e:
                    print(
                        self.red(f"[!]  Invalid Choice Entered! | "),
                        self.lmagenta(str(e)),
                    )
                    sys.exit(1)
                except IndexError as e:
                    print(
                        self.red(f"[!]  This Episode / Movie is coming soon! | "),
                        self.lmagenta(str(e)),
                    )
                    sys.exit(2)
            else:
                selection = result[int(choice) - 1]
                if selection[-1] == "TV":
                    cdnurl, name = self.ask(selection[2], selection[0])
                    self.play(cdnurl, name)
                else:
                    cdn, name = self.cdn_url(selection[0])
                    self.play(cdn, name)

    def redo(self, query: str = None, result: int = None):
        if query is None:
            return self.display(self.search())
        else:
            return self.display(self.search(query))

# f = OlgPly()
# OlgPly.cdnurl(OlgPly.search()[0][2])

## Has not been edited since olgply is down
