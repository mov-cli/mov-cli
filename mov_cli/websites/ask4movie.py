from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re
import base64
import httpx
class Ask4Movie(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q: str = None):
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        print("Don't use the Seasons labeled as MOVIE, it will not work.")
        return q.replace(" ", "+")  
    
    def results(self, q):
        res = self.client.get(f"{self.base_url}/?s={q}")
        soup = BS(res.text, "lxml")
        result = soup.findAll("div", {"class": "item"})
        def checkmov(x):
            if result[x].findAll("a")[1]["href"].__contains__("channel"):
                return "TV"
            elif result[x].findAll("a")[1]["href"].__contains__("season"):
                return "TV"
            else:
                return "MOVIE"
        ids = [i for i in range(len(result))]
        title = [result[i].findAll("a")[1].text for i in range(len(result))]
        urls = [result[i].findAll("a")[1]["href"] for i in range(len(result))]
        mov_or_tv = [checkmov(i) for i in range(len(result))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def get_link(self, url):
        res = self.client.get(url).text
        reg= re.findall("""<script src="data:text\/javascript;base64,([^"']*)""", res)[1]
        txt = base64.b64decode(reg)
        text = txt.decode("utf-8")
        regs = re.findall("""dir['"],['"]([^"']*)""", text)[0]
        txt = base64.b64decode(regs)
        txt = txt.decode("utf-8")
        soup = BS(txt, "lxml")
        reslink = soup.find("iframe")["src"]
        reslink = reslink.split("/")[4]
        return reslink

    def ask_direct_season(self, show_url):
        reslink = self.get_link(show_url)
        res = self.client.get(f"https://cinegrabber.com/p/{reslink}").text
        soup = BS(res, "lxml")
        season = soup.title.text.split("┋")[1][1:]
        episodes = soup.findAll("span", {"class": "episode"})
        episode = int(input(
            self.lmagenta(
                f"Please input the episode number(total episodes in season:{season}):{len(episodes)}: "
            )
        ))
        url = episodes[episode - 1]["data-url"].split("/")[2]
        return url, season, episode

    def ask_season(self, show_url):
        res = self.client.get(show_url)
        soup = BS(res, "lxml")
        seasons = soup.findAll("div", {"class": "item"})
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{len(seasons)}): "
        ))
        season = seasons[len(seasons) - int(season)]
        seasonlink = season.find("a")["href"]
        reslink = self.get_link(seasonlink)
        res = self.client.get(f"https://cinegrabber.com/p/{reslink}").text
        soup = BS(res, "lxml")
        season = soup.title.text.split("┋")[1][1:]
        episodes = soup.findAll("span", {"class": "episode"})
        episode = int(
            input(
                self.lmagenta(
                    f"Please input the episode number(total episodes in season:{season}):{len(episodes)}: "
                )
        ))
        url = episodes[episode - 1]["data-url"].split("/")[2]
        return url, season, episode
    
    def movie(self, url):
        return self.get_link(url)
    
    def cdn_url(self, url):
        postheaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0", "Referer": f"https://cinegrabber.com/v/{url}", "Origin": "https://cinegrabber.com"}
        url = f"https://cinegrabber.com/api/source/{url}"
        res = httpx.post(url, headers=postheaders).json()
        print(url)
        url = res["data"][len(["data"]) + 1]["file"]
        print(url)
        return url
    
    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if t[self.url].__contains__("channel"):
            url, season, episode = self.ask_season(t[self.url])
        else:
            url, season, episode = self.ask_direct_season(t[self.url])
        name = t[self.title]
        url = self.cdn_url(url)
        # History.addhistory(self.userinput, state, "", season)
        if state == "d":
            self.dl(url, name, episode=episode, season=season)
            return
        # update_presence(t[self.title], season)
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url =self.movie(m[self.url])
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name)
            return
        if state == "sd":
            print("You can download only Shows with 'sd'")
            return
        self.play(url, name)
    
    def SandR(self, q: str = None):
        return self.results(self.search(q))



