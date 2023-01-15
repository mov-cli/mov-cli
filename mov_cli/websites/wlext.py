from bs4 import BeautifulSoup as BS
from ..utils.scraper import WebScraper
import re

class wlext(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q: str = None) -> list:
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q.replace(" ", "+")
    
    def results(self, data: str) -> list:
        print("Is it an Movie or a Show?\r\n[1] Movie\r\n[2] Show")
        question = input("Enter: ")
        if question == "1":
            m = self.client.get(f"{self.base_url}/ptb-search/?f=search_movies&ptb-search=1&title={data}")
            movie = BS(m, "lxml")
            movies = movie.findAll("h5", {"class": "ptb_post_title"})
            urls = [movies[i].find("a")["href"] for i in range(len(movies))]
            title = [movies[i].find("a").text for i in range(len(movies))]
            ids = [i for i in range(len(movies))]
            mov_or_tv = ["TV" for i in range(len(movies))]
        else:
            s = self.client.get(f"{self.base_url}/ptb-search/?f=search_series_1&ptb-search=1&title={data}")
            show = BS(s, "lxml")
            shows = show.findAll("h5", {"class": "ptb_post_title"})
            urls = [shows[i].find("a")["href"] for i in range(len(shows))]
            title = [shows[i].find("a").text for i in range(len(shows))]
            ids = [i for i in range(len(shows))]
            mov_or_tv = ["TV" for i in range(len(shows))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def ask(self, url):
        req = self.client.get(url)
        soup = BS(req, "lxml")
        t = soup.find("select", {"id": "loadepisode"})
        try:
            episodes = len(t.findAll("option"))
        except:
            return print("Episode unavailable")
        episode = int(
            input(
                self.lmagenta(
                    f"Please input the episode number(Total: {episodes}): "
                    )
                )
            )
        req = self.client.get(f"{url}?server=cajitatop&episode={episode}").text
        soup = BS(req, "lxml")
        try:
            t = soup.find("iframe", {"loading": "lazy"})["src"]
        except:
            return print("Couldn't find cajita.to provider.")
        return t, episode
    
    def cdn_url(self, url):
        self.client.set_headers({"origin": "cajita.top", "referer": f"{url}"})
        string = re.findall("""v\/([^"']*)""", url)[0]
        request = self.client.post(f"https://cajita.top/api/source/{string}", data={"r": f"{self.base_url}", "d": "cajita.top"}).json()
        file = request["data"]
        if file == "Video not found or has been removed":
            print("Video not found or has been removed")
            exit(1)
        else:
            file = request["data"][-1]["file"]
            file = self.client.get(file).url
        return file
    
    
    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode = self.ask(t[self.url])
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name, season=".", episode=episode)
            return
        self.play(url, name)
    
    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url, episode = self.ask(f"{m[self.url]}")
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)