from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re

class trailers(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url


    def search(self, q: str = None):
        q =( 
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        q = re.sub('\W+',' ', q)
        return q.replace(" ", "+")

    def results (self, q: str) -> list:
        t = self.client.get(f"https://trailers.to/en/popular/movies-tvshows-collections?q={q}").text
        soup = BS(t, "lxml")
        lis = soup.findAll("article", {"class": "tour-modern list-item"})
        ids = [lis[i].find("a")["href"].split("/")[2] for i in range(len(lis))]
        title = [lis[i]["id"] + ", " + 
        lis[i].findAll("span", {"class": "small-text font-weight-sbold"})[1].text + 
        "," for i in range(len(lis))]
        urls = [lis[i].find("a")["href"] for i in range(len(lis))]
        mov_or_tv = ["TV" if lis[i].find("a")["href"].__contains__("tvshow") else "MOVIE" for i in range(len(lis))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def ask(self, url: str):
        re = self.client.get(f"https://trailers.to{url}").text
        soup = BS(re, "lxml")
        seasons = soup.findAll("div", {"class": "collapse"})
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{len(seasons)}): "
        ))
        episodes = seasons[int(season) - 1].findAll("article", {"class": "tour-modern"})
        episode = input(
            self.lmagenta(
                f"Please input the episode number(total episodes in season:{season}):{len(episodes)}: "
            )
        )
        return season, episode
        
    def shows_cdn_url(self, season, episode, link):
        re = self.client.get(f"https://trailers.to{link}").text
        soup = BS(re, "lxml")
        seasons = soup.findAll("div", {"class": "collapse"})[int(season) - 1]
        episode = seasons.findAll("article", {"class": "tour-modern"})[int(episode) - 1].find("a")["href"]
        res = self.client.get(f"https://trailers.to{episode}").text
        soup = BS(res, "lxml") 
        url = soup.find("a", {"id": "download-button"})["href"]
        print(url)
        return url
    
    def mov_cdn_url(self, link):
        re = self.client.get(f"https://trailers.to{link}").text
        soup = BS(re, "lxml")
        url = soup.find("a", {"id": "download-button"})["href"]
        print(url)
        return url

    def showdownload(self, t):
        re = self.client.get(f"https://trailers.to{url}").text
        soup = BS(re, "lxml")
        seasons = soup.findAll("div", {"class": "collapse"})
        for s in range(len(seasons)):
            episodes = seasons[s].findAll("article", {"class": "tour-modern"})
            for e in range(len(episodes)):
                name = t[self.title]
                url = self.shows_cdn_url(s, e, t[self.url])
                self.dl(url, name, season=s+1, episode=e+1)
    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            self.showdownload(t)
            return
        name = t[self.title]
        season, episode = self.ask(t[self.url])
        url = self.shows_cdn_url(season, episode, t[self.url])
        #History.addhistory(self.userinput, state, "", season)
        if state == "d":
            self.dl(url, name, season=season, episode=episode)
            return
        #update_presence(t[self.title], season)
        print("Seeking is Disabled with Trailers")
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url = self.mov_cdn_url(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        if state == "sd":
            print("You can download only Shows with 'sd'")
            return
        print("Seeking is Disabled with Trailers")
        self.play(url, name)
