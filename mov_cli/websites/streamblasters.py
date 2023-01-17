from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
import re

class streamblasters(WebScraper):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q):
        q = input(self.blue("[!] Please Enter the name of the Movie: "))
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        req = self.client.get(f"{self.base_url}/?s={data}")
        soup = BS(req, "lxml")
        items = soup.findAll("div", {"class": "title"})
        urls = [items[i].find("a")["href"] for i in range(len(items))]
        title = [items[i].find("a").text for i in range(len(items))]
        ids = [i for i in range(len(items))]
        mov_or_tv = ["MOVIE" for i in range(len(items))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]
    
    def doodext(self, url):
        req = self.client.get(url).text
        soup = BS(req, "lxml")
        ply = soup.find("li", {"id": "player-option-1"})
        post = ply["data-post"]
        self.client.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Referer": f"{url}", "Accept-Language":"de,en-US;q=0.7,en;q=0.3"})
        data = {
            "action": "doo_player_ajax",
            "post": post,
            "nume": "1",
            "type": "movie"
        }
        post = self.client.post(f"{self.base_url}/wp-admin/admin-ajax.php", data=data).text
        try:
            src = re.findall('''"https:(.*?)"''', post)[0].replace("\/", "/")
        except:
            raise Exception("No URL was found")
        if "\\" in src:
            src = src.replace("\\", "")
        src = f"https:{src}"
        print(src)
        return src

    def doodstream(self, url):
        domain = re.findall("""([^"']*)\/e""", url)[0]
        red = self.client.get(url).headers
        redirect = re.findall("""\('location', '(.*?)'\)""", str(red))[0]
        req = self.client.get(f"{domain}{redirect}").text
        pass_md = re.findall(r"/pass_md5/[^']*", req)[0]
        token = pass_md.split("/")[-1]
        self.client.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Referer": f"{url}", "Accept-Language": "en-GB,en;q=0.5"})
        drylink = self.client.get(f"{domain}{pass_md}").text
        streamlink = f"{drylink}zUEJeL3mUN?token={token}"
        print(streamlink)
        return streamlink

    def MOV_PandDP(self, m: list, state: str = "d" or "p"):
        name = m[self.title]
        url = self.doodext(m[self.url])
        url = self.doodstream(url)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name,)

