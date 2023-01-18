from ..utils.scraper import WebScraper
from ..utils.httpclient import default_header
from bs4 import BeautifulSoup as BS
import re
import httpx
from ..utils import jsunpack

class kinox(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q: str):
        q = (
            input(self.blue("[!] Please Enter the name of the Movie: "))
            if q is None
            else q
        )
        return q.replace(" ", "+")
    
    def comp(self, element):
        title = element.find("a").text
        lang = element.find("img", {"alt": "language"})["src"]
        year = element.find("span", {"class": "Year"}).text
        if "1" in lang:
            lang = "Ger"
        elif "15" in lang:
            lang = "Ger/Eng"
        else:
            lang = "Eng"
        title = f"{lang} | {title} | {year}"
        return title
    
    def mov_or_tv(self, element):
        ele = element.find("img", {"alt":"type"})["title"]
        if ele == "series":
            return "TV"
        elif ele == "movie":
            return "MOVIE"
        else:
            return "TV"

    def results(self, data: str):
        request = self.client.get(f"{self.base_url}/Search.html?q={data}")
        soup = BS(request, "lxml")
        streams = soup.find("tbody").findAll("tr")
        urls = [streams[i].find("a")["href"] for i in range(len(streams))]
        title = [self.comp(streams[i]) for i in range(len(streams))]
        ids = [i for i in range(len(streams))]
        mov_or_tv = [self.mov_or_tv(streams[i]) for i in range(len(streams))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def voe(self, url):
        regex = r'"<a href=\\"(.*?)"'
        html = self.client.get(url).text
        url = re.findall(regex, html)[0].replace("\/", "/").replace("\\", "")
        redirect = self.client.head(url, redirects=False).headers.get("location")
        req = self.client.get(redirect).text
        reg = """'mp4': '(.*)'"""
        link = re.findall(reg,req)[0]
        return link
    
    def get_packed_data(self, html):
        packed_data = ''
        for match in re.finditer(r'(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
            if jsunpack.detect(match.group(1)):
                packed_data += jsunpack.unpack(match.group(1))

        return packed_data

    def streamz(self, link):
        reg = r'"<a href=\\"(.*?)"'
        t = self.client.get(link).text
        url = re.findall(reg, t)[0].replace("\/", "/").replace("\\", "")
        print(url)
        url = self.client.head(url, redirects=True).url
        html = self.client.get(str(url)).text
        if '<b>File not found, sorry!</b>' not in html:
            html += self.get_packed_data(html)
            v = re.search(r"player\s*=\s*.*?'([^']+)", html)
            if v:
                vurl = re.search(r'''{0}".+?src:\s*'([^']+)'''.format(v.group(1)), html)
                if vurl:
                    url = self.client.head(vurl.group(1), redirects=False).headers.get("location")
                    return url
        raise Exception('Video not found or removed')
    
    def ask(self, url):
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, "lxml")
        select = soup.find("select",{"id": "SeasonSelection"}).findAll("option")
        season = int(
            input(
                self.lmagenta(
                    f"Please input the season number(total seasons:{len(select)}): "
                )
            )
        )
        option = select[season - 1]["rel"].split(",")
        print(option)
        episode = int(
            input(
                self.lmagenta(
                    f"Please input the episode number(total episodes in season:{season}):{len(option)} : "
                )
            )
        )
        option = option[episode - 1]
        name = re.findall("\/Stream\/(.*)\.", url)[0]
        try:
            url = self.voe(f"{self.base_url}/aGET/Mirror/{name}&Hoster=92&Season={season}&Episode={option}")
        except:
            url = self.streamz(f"{self.base_url}/aGET/Mirror/{name}&Hoster=88&Season={season}&Episode={option}")
        return url, episode, season
    
    def movie(self, url):
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, "lxml")
        name = re.findall("\/Stream\/(.*)\.", url)[0]
        try:
            soup.find("li", {"id": "Hoster_92"})
            url = self.voe(f"{self.base_url}/aGET/Mirror/{name}&Hoster=92")
        except:
            url = self.streamz(f"{self.base_url}/aGET/Mirror/{name}&Hoster=88")
        return url

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.movie(m[self.url])
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name,)
    
    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode, season = self.ask(t[self.url])
        if state == "d":
            self.dl(url, name, season=season, episode=episode)
            return
        self.play(url, name)
