import re
import sys
import json
import httpx

sys.path.append("..")
from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS


class Theflix(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.token = self.auth_token()
        self.aid = 1
        self.m_available = -3
        self.t_available = -2
        self.seasons = -1
        self.userinput = ""

    def parse(self, text: str):
        name = f"{text[0].lower()}{''.join([f' {i}' if i.isupper() else i for i in text[1:]]).lower().rstrip('.')}"
        return re.sub("\W+", "-", name)
    def auth_token(self):
        return httpx.post(
            "https://theflix.to:5679/authorization/session/continue?contentUsageType=Viewing",
            data={"affiliateCode": "", "pathname": "/"},
        ).headers["Set-Cookie"]

    def search(self, query: str = None) -> list:
        print(self.red("[s] Search"))
        print(self.red("[ts] Trending TV Shows"))
        print(self.red("[tm] Trending Movies"))
        print(self.red("[q] Quit"))
        choice = input(self.blue("Enter your choice: ")).lower()
        if choice == "s":
            q = (
                input(self.blue("[!] Please Enter the name of the Movie: "))
                if query is None
                else query
            )
            data = []
            for j in [
                [self.parse(i["name"]), i["id"], i["available"], "TV", i["numberOfSeasons"]]
                for i in json.loads(
                    BS(
                        self.client.get(f"https://theflix.to/tv-shows/trending?search={q}"),
                        "lxml",
                    )
                    .select("#__NEXT_DATA__")[0]
                    .text
                )["props"]["pageProps"]["mainList"]["docs"]
                if i["available"]
            ]:
                data.append(j)
            for k in [
                [self.parse(i["name"]), i["id"], "MOVIE", i["available"]]
                for i in json.loads(
                    BS(
                        self.client.get(
                            f"https://theflix.to/movies/trending?search={q.replace(' ', '+')}"
                        ),
                        "lxml",
                    )
                    .select("#__NEXT_DATA__")[0]
                    .text
                )["props"]["pageProps"]["mainList"]["docs"]
                if i["available"]
            ]:
                data.append(k)
            if not len(data):
                print(self.red("No Results found"), self.lmagenta("Bye!"))
                sys.exit(1)
            else:
                return data
        elif choice == "ts":
            return self.trendingtvshows()
        elif choice == "tm":
            return self.trendingmovies()
        elif choice == "q":
            print(self.red("Bye!"))
            sys.exit(1)

    def trendingtvshows(self):
        data = []
        for j in [
            [self.parse(i["name"]), i["id"], i["available"], "TV", i["numberOfSeasons"]]
            for i in json.loads(
                BS(
                    self.client.get(f"https://theflix.to/tv-shows/trending"),
                    "lxml",
                )
                .select("#__NEXT_DATA__")[0]
                .text
            )["props"]["pageProps"]["mainList"]["docs"]
            if i["available"]
        ]:
            data.append(j)
        return data
    
    def trendingmovies(self):
        data = []
        for k in [
            [self.parse(i["name"]), i["id"], "MOVIE", i["available"]]
            for i in json.loads(
                BS(
                    self.client.get(
                        f"https://theflix.to/movies/trending"
                    ),
                    "lxml",
                )
                .select("#__NEXT_DATA__")[0]
                .text
            )["props"]["pageProps"]["mainList"]["docs"]
            if i["available"]
        ]:
            data.append(k)
        return data

    def page(self, info):
        return f"{self.base_url}/movie/{info[1]}-{info[0]}", info[0]

    def wspage(self, info):
        return (
            f"{self.base_url}/tv-show/{info[1]}-{info[0]}/season-{info[-2]}/episode-{info[-1]}",
            f"{info[0]}_S_{info[-2]}_EP_{info[-1]}",
        )

    def cdnurl(self, link, info, k):
        self.client.set_headers({"Cookie": k})
        objid = json.loads(
            BS(self.client.get(link).text, "lxml")
            .select("#__NEXT_DATA__")[0]
            .text
        )["props"]["pageProps"]["movie"]["videos"][0]
        self.client.set_headers({"Cookie": k})
        link = self.client.get(
            f"https://theflix.to:5679/movies/videos/{objid}/request-access?contentUsageType=Viewing"
        ).json()["url"]
        return link, info

    def get_season_episode(self, link):
        return (
            re.search(r"(?<=season-)\d+", link).group(),
            re.search(r"(?<=episode-)\d+", link).group(),
        )

    def cdnurlep(self, link, info, k):
        s, ep = self.get_season_episode(link)
        self.client.set_headers({"Cookie": k})
        f = json.loads(
            BS(self.client.get(link).text, "lxml")
            .select("#__NEXT_DATA__")[0]
            .text
        )["props"]["pageProps"]["selectedTv"]["seasons"]
        try:
            epid = f[int(s) - 1]["episodes"][int(ep) - 1]["videos"][0]
        except IndexError:
            print(
                self.red("Episode unavailable"),
                self.lmagenta("Bye!"),
                self.blue(
                    "Maybe try "
                    "one of the "
                    "other "
                    "websites or "
                    "request the "
                    "episode to "
                    "be added by "
                    "contacting "
                    "theflix"
                ),
            )
            sys.exit()
        self.client.set_headers({"Cookie": k})
        link = self.client.get(
            f"https://theflix.to:5679/tv/videos/{epid}/request-access?contentUsageType=Viewing"
        ).json()["url"]
        return link, info

    def ask(self, ts, ids, name, tok):
        season = input(
            self.lmagenta(f"Please input the season number(total seasons:{ts}): ")
        )
        self.client.set_headers({"cookie": tok})
        episodes = json.loads(
            BS(
                self.client.get(
                    f"https://theflix.to/tv-show/{ids}-{name}/season-{season}/episode-1"
                ),
                "lxml",
            )
            .select("#__NEXT_DATA__")[0]
            .text
        )["props"]["pageProps"]["selectedTv"]["numberOfEpisodes"]
        episode = input(
            self.lmagenta(
                f"Please input the episode number(total episodes in {season}:{episodes // int(ts)}: "
            )
        )
        return season, episodes, episode

    """def display(self, result: list, result_no: int = None):
        print(result_no)
        for ix, vl in enumerate(result):
            print(self.green(f"[{ix + 1}] {vl[0]} {vl[-1]}"), end="\n\n")
        print(self.red("[q] Exit!"), end="\n\n")
        print(self.yellow("[s] Search Again!"), end="\n\n")
        print(self.cyan("[d] Download!"), end="\n\n")
        choice = ""
        while choice not in range(len(result) + 1):
            choice = (
                input(self.blue("Enter your choice: ")) if not result_no else result_no
            )
            if choice == "q":
                sys.exit()
            elif choice == "s":
                return self.redo()
            elif choice == "d":
                token = self.auth_token()
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
                    if mov[-1] == "WS":
                        season, episodes, episode = self.ask(
                            mov[-2], mov[1], name, token
                        )
                        page, name = self.wspage([mov[0], mov[1], season, episode])
                        cdn, name = self.cdnurlep(page, name, token)
                        self.dl(cdn, name)
                    else:
                        page = self.page(mov)
                        cdn, name = self.cdnurl(page[0], name, token)
                        self.dl(cdn, name)
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
                token = self.auth_token()
                selection = result[int(choice) - 1]
                if selection[-1] == "WS":
                    season, episodes, episode = self.ask(
                        selection[-2], selection[1], selection[0], token
                    )
                    page, name = self.wspage(
                        [selection[0], selection[1], season, episode]
                    )
                    cdn, name = self.cdnurlep(page, name, token)
                    self.play(cdn, name)
                else:
                    page = self.page(selection)
                    cdn, name = self.cdnurl(page[0], selection[0], token)
                    self.play(cdn, name)"""

    def SandR(self, q: str = None):
        return self.search(q)

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        self.userinput = f"{name}"
        page = self.page(m)
        url, name = self.cdnurl(page[0], name, self.token)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)

    def TV_PandDP(self, t: list, state: str = "d" or "p"):
        name = t[self.title]
        season, episodes, episode = self.ask(
            t[self.seasons], t[self.aid], name, self.token
        )
        self.userinput = f"{name}"
        page, name = self.wspage([name, t[1], season, episode])
        cdn, name = self.cdnurlep(page, name, self.token)
        if state == "d":
            self.dl(cdn, name)
            return
        self.play(cdn, name)

    # def redo(self, query: str = None, result: int = None):
    #    if query is None:
    #        return self.display(self.search(), result)
    #    else:
    #        return self.display(self.search(query), result)
