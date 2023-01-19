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
        self.base_url = self.client.head("https://kinox.to", redirects=False).headers.get("location")[:-1]
        request = self.client.get(f"{self.base_url}/Search.html?q={data}").text
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
        if "404 - Page not found" not in req:
            reg = """'mp4': '(.*)'"""
            link = re.findall(reg,req)[0]
            return link
        raise Exception('Video not found or removed')
        
    def doodstream(self, url):
        regex = r'"<a href=\\"http:\\\/\\\/[a-z]+.[a-z]+\\\/d\\\/(.*?)\\'
        html = self.client.get(url).text
        url = re.findall(regex, html)[0]
        req = self.client.get(f"https://dood.wf/e/{url}").text
        pass_md = re.findall(r"/pass_md5/[^']*", req)[0]
        token = pass_md.split("/")[-1]
        self.client.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Referer": f"https://dood.wf/e/{url}", "Accept-Language": "en-GB,en;q=0.5"})
        drylink = self.client.get(f"https://dood.wf{pass_md}").text
        streamlink = f"{drylink}zUEJeL3mUN?token={token}"
        print(streamlink)
        return streamlink
    
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
                    self.client.set_headers({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', 'Accept-Language': 'en-GB,en;q=0.5', 'Referer': f'https://streamz.ws/', "sec-fetch-dest": "video"})
                    url = self.client.head(vurl.group(1), redirects=False).headers.get("location")
                    return url
        raise Exception('Video not found or removed')
    
    def ask(self, url):
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, "lxml")
        select = soup.find("select",{"id": "SeasonSelection"}).findAll("option")
        rel = soup.find("select",{"id": "SeasonSelection"})["rel"]
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
        hostlist = self.client.get(f"{self.base_url}/aGET/MirrorByEpisode/{rel}&Season={season}&Episode={option}").text
        name = re.findall("\/Stream\/(.*)\.", url)[0]
        if re.search("Hoster_92", hostlist):
            url = self.voe(f"{self.base_url}/aGET/Mirror/{name}&Hoster=92&Season={season}&Episode={option}")
        elif re.search("Hoster_95", hostlist):
            url = self.doodstream(f"{self.base_url}/aGET/Mirror/{name}&Hoster=95&Season={season}&Episode={option}")
        else:
            url = self.streamz(f"{self.base_url}/aGET/Mirror/{name}&Hoster=88&Season={season}&Episode={option}")
        return url, episode, season
    
    def movie(self, url):
        req = self.client.get(f"{self.base_url}{url}").text
        soup = BS(req, "lxml")
        name = re.findall("\/Stream\/(.*)\.", url)[0]
        try:
            if re.search("Hoster_92", req):
                url = self.voe(f"{self.base_url}/aGET/Mirror/{name}&Hoster=92")
            elif re.search("Hoster_95", req):
                url = self.doodstream(f"{self.base_url}/aGET/Mirror/{name}&Hoster=95")
            else:
                url = self.streamz(f"{self.base_url}/aGET/Mirror/{name}&Hoster=88")
        except Exception as e:
            url = self.streamz(f"{self.base_url}/aGET/Mirror/{name}&Hoster=88")
            print(e)
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
