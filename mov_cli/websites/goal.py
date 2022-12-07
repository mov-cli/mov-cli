from ..utils.scraper import WebScraper
from bs4 import BeautifulSoup as BS
from datetime import datetime

class goal9(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
    
    def search(self, q):
        q = "q"
        return q

    def results(self, q):
        dataid = self.client.get("https://justameanlessdomain.com/v1/match/related").json()["data"][0]["id"]
        res = self.client.get(f"https://justameanlessdomain.com/v1/match/{dataid}").json()
        name = res["data"]["name"]
        streamdata = self.client.get(f"https://justameanlessdomain.com/v1/match/{dataid}/stream").json()
        streams = streamdata["data"]["play_urls"]
        urls = [streams[i]["url"] for i in range(len(streams))]
        title = [streams[i]["name"] for i in range(len(streams))]
        ids = [streams[i]["role"] for i in range(len(streams))]
        mov_or_tv = [f"{name}" for i in range(len(streams))]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    
    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        if state == "sd":
            print("You can't Showdownload Football Match!?") # IF you call it soccer you clearly have made something wrong in life
            return
        if state == "d":
            self.dl(m[self.url], m[self.title])
            return
        self.play(m[self.url], m[self.title])
        
    def SandR(self, q: str = None):
        return self.results(self.search(q))





