import re
import sys
import json
import base64
from urllib import parse as p

from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS

sys.path.append("..")


x = lambda d: base64.b64encode(d.encode()).decode().replace("\n", "").replace("=", ".")


class Actvid(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.rep_key = (
            "6LfV6aAaAAAAAC-irCKNuIS5Nf5ocl5r0K3Q0cdz"  # Google Recaptcha key
        )
        self.rab_domain = x(
            "https://rabbitstream.net:443"
        )  # encoding and then decoding the url
        # self.redo()
        ##IMP: self.client.get/post always returns a response object
        # self.client.post/get -> httpx.response

    def key_num(self, iframelink):
        self.client.add_elem("referer", self.base_url)  # adding referer to the headers
        # self.client.headers['Referer'] = self.base_url
        req = self.client.get(iframelink).text
        soup = BS(req, "html.parser")
        k = list([i.text for i in soup.find_all("script")][-3].replace("var", ""))
        key = "".join(k[21:61])
        num = k[-3]
        return key, num  # returns a tuple

    def auth_token(self, key: str) -> str:
        # self.client.set_headers({'referer': self.__base_url, 'cacheTime': '0'})
        # self.client.headers['Referer'] = self.base_url
        self.client.add_elem("referer", self.base_url)  # adding referer to the headers
        self.client.add_elem("cacheTime", "0")  # adding referer to the headers
        # self.client.headers['cacheTime'] = '0'
        r = self.client.get(
            f"https://www.google.com/recaptcha/api.js?render={self.rep_key}"
        )
        s = r.text.replace("/* PLEASE DO NOT COPY AND PASTE THIS CODE. */", "")
        s = s.split(";")
        vtoken = s[10].replace("po.src=", "").split("/")[-2]
        r = self.client.get(
            f"https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=xxmovclix&k={key}&co={self.rab_domain}&v={vtoken}"
        ).text
        soup = BS(r, "html.parser")
        recap_token = [i["value"] for i in soup.select("#recaptcha-token")][0]
        data = {
            "v": vtoken,
            "k": self.rep_key,
            "c": recap_token,
            "co": self.rab_domain,
            "sa": "",
            "reason": "q",
        }
        self.client.set_headers({"cacheTime": "0"})
        return json.loads(
            self.client.post(
                f"https://www.google.com/recaptcha/api2/reload?k={key}", data=data
            ).text.replace(")]}'", "")
        )

    def search(self, query: str = None) -> str:
        query = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if query is None
            else query
        )
        return self.client.get(f"{self.base_url}/search/{self.parse(query)}").text

    def results(self, html: str) -> list:
        soup = BS(html, "html.parser")
        urls = [i["href"] for i in soup.select(".film-poster-ahref")]
        mov_or_tv = [
            "MOVIE" if i["href"].__contains__("/movie/") else "TV"
            for i in soup.select(".film-poster-ahref")
        ]
        title = [
            re.sub(
                pattern="full|/tv/|/movie/|hd|watch|[0-9]{2,}",
                repl="",
                string=" ".join(i.split("-")),
            )
            for i in urls
        ]
        ids = [i.split("-")[-1] for i in urls]
        return [list(sublist) for sublist in zip(mov_or_tv, urls, title, ids)]
        # ?An object of the result list contains a list that contains [1]Movie or Tv [2]Url of the thing [3]Title of
        # the thing [4]Id of the thing

    def ask(self, series_id) -> str:
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "html.parser").select(".dropdown-item")
        ]
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{len(season_ids)}): "
            )
        )
        x = f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        rf = self.client.get(x)
        episodes = [i["data-id"] for i in BS(rf, "html.parser").select(".nav-item > a")]
        episode = episodes[
            int(
                input(
                    self.lmagenta(
                        f"Please input the episode number(total episodes in season:{season}):{len(episodes)} : "
                    )
                )
            )
            - 1
        ]
        return episode

    def cdn_url(self, rabbid, rose, num) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(
            f"https://mzzcloud.life/ajax/embed-4/getSources?id={rabbid}&_token={rose}&_number={num}"
        ).json()["sources"][0]["file"]
        return data

    def display(self, result: list):
        for ix, vl in enumerate(result):
            print(self.green(f"[{ix + 1}] {vl[2]} {vl[0]}"), end="\n\n")
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
                    # mov = result[int(choice) - 1]
                    name = mov[2]
                    if mov[0] == "TV":
                        episode = self.ask(mov[3])
                        sid = self.ep_server_id(episode)
                        iframe_url, mov_id = self.get_link(sid)
                        key, num = self.key_num(iframe_url)
                        token = self.auth_token(key)[1]
                        url = self.cdn_url(mov_id, token, num)
                        self.dl(url, name)
                    else:
                        sid = self.server_id(mov[3])
                        iframe_url, mov_id = self.get_link(sid)
                        key, num = self.key_num(iframe_url)
                        token = self.auth_token(key)[1]
                        url = self.cdn_url(mov_id, token, num)
                        self.dl(url, name)
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
                mov = result[int(choice) - 1]
                name = mov[2]
                if mov[0] == "TV":
                    episode = self.ask(mov[3])
                    sid = self.ep_server_id(episode)
                    iframe_url, mov_id = self.get_link(sid)
                    key, num = self.key_num(iframe_url)
                    token = self.auth_token(key)[1]
                    url = self.cdn_url(mov_id, token, num)
                    self.play(url, name)
                else:
                    sid = self.server_id(mov[3])
                    iframe_url, mov_id = self.get_link(sid)
                    key, num = self.key_num(iframe_url)
                    token = self.auth_token(key)[1]
                    url = self.cdn_url(mov_id, token, num)
                    self.play(url, name)

    def server_id(self, mov_id) -> str:
        req = self.client.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = BS(req, "html.parser")
        return [i["data-linkid"] for i in soup.select(".nav-item > a")][0]

    def ep_server_id(self, ep_id) -> str:
        req = self.client.get(
            f"{self.base_url}/ajax/v2/episode/servers/{ep_id}/#servers-list"
        )
        soup = BS(req, "html.parser")
        return [i["data-id"] for i in soup.select(".nav-item > a")][0]

    def get_link(self, thing_id):
        req = self.client.get(f"{self.base_url}/ajax/get_link/{thing_id}").json()[
            "link"
        ]
        print(req)
        return req, self.rabbit_id(req)

    def rabbit_id(self, url: str):
        return p.urlparse(url, allow_fragments=True, scheme="/").path.split("/")[-1]

    def redo(self, query: str = None):
        if query is None:
            return self.display(self.results(self.search()))
        else:
            return self.display(self.results(self.search(query)))
