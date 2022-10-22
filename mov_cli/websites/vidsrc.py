from bs4 import BeautifulSoup as BS
import os
import threading
import sys
from ..utils.scraper import WebScraper
from ..utils.keep_alive import KP

sys.path.append("..")
import httpx


class Vidsrc(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.stream = "https://vidsrc.stream/pro/"
        self.streamh = {"Referer": "https://source.vidsrc.me/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
        self.headers = {"Referer": "https://v2.vidsrc.me",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
        self.finalheaders = {"Referer": "https://vidsrc.stream/", "Origin": "https://vidsrc.stream",
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
        self.keep_alive = KP(self.stream)

    def search(self, q: str = None):
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q

    def results(self, html: str) -> list:
        data = httpx.get(f"https://v2.sg.media-imdb.com/suggestion/{html[0]}/{html}.json", headers=self.headers).json()
        ids = [data["d"][i]["id"] for i in range(len(data["d"]))]
        title = [data["d"][i]["l"] for i in range(len(data["d"]))]
        urls = ["/embed/" + data["d"][i]["id"] for i in range(len(data["d"]))]
        def movtv(num):
            try:
                if data["d"][num]["qid"].__contains__("tvSeries"):
                    return "TV"  
                else:
                    return "MOVIE"
            except:
                return "UNKNOWN"
                    
        mov_or_tv =[movtv(i) for i in range(len(data["d"]))]
        
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def get_playeriframe(self, embed):
        url = self.base_url + embed
        re = httpx.get(url, headers=self.headers)
        print(url)
        soup = BS(re, "lxml")
        iframe = soup.find("iframe", {"id": "player_iframe"})
        iframe = iframe["src"]
        iframe = iframe.split("/")[4]
        return iframe

    def ask(self, imdb: str):
        re = self.client.get(f"https://www.imdb.com/title/{imdb}/episodes")
        soup = BS(re, "lxml")
        seasons = soup.find("h3", {"id": "episode_top"}).text.strip("Season")
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{seasons}): "
            ))
        z = self.client.get(f"https://www.imdb.com/title/{imdb}/episodes?season={season}")
        episodes = soup.findAll("div", {"class": "list_item"})
        episode = input(
            self.lmagenta(
                f"Please input the episode number(total episodes in season:{season}):{len(episodes)}: "
            )
        )
        return season, episode

    def cdn_url(self, iframe):
        stream = self.stream + iframe
        re = httpx.get(stream, headers=self.streamh).text
        soup = BS(re, "lxml")
        scripts = soup.find_all("script")
        script = scripts[7]
        script = "".join(script)
        path = script.split("=")[4]
        actlink = script.split("=")[3]
        actlink = actlink.split('"')[1]
        path = path.split('"')[0]
        actlink = "https:" + actlink + "=" + path
        print(actlink)
        url = script.split("/")
        url = "https://" + url[19] + "/" + url[20] + "/" + url[21] + "/index-v1-a1.m3u8"
        t1 = threading.Thread(target=self.keep_alive.ping, args=(actlink, self.finalheaders))
        t1.start()
        return url, actlink

    def enabler(self, path):
        test = httpx.get(path, headers=self.finalheaders).text
        return

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        season, episode = self.ask(t[self.aid])
        iframe = self.get_playeriframe(f"{t[self.url]}/{season}-{episode}")
        url, enable = self.cdn_url(iframe)
        self.enabler(enable)
        print(url)
        # History.addhistory(self.userinput, state, "", season)
        if state == "d":
            self.dl(url, name)
            return
        # update_presence(t[self.title], season)
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        iframe = self.get_playeriframe(f"{m[self.url]}")
        url, enable = self.cdn_url(iframe)
        self.enabler(enable)
        if state == "d":
            self.dl(url, name)
            return
        if state == "sd":
            print("You can download only Shows with 'sd'")
            return
        self.play(url, name)

    def SandR(self, q: str = None):
        return self.results(self.search(q))
