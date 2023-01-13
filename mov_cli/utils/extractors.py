from .httpclient import HttpClient
from bs4 import BeautifulSoup as BS
import re


class Extractors():
    def __init__(self):
        self.client = HttpClient()

    def doodstream(self, url):
        domain = re.findall("""([^"']*)\/e""", url)[0]
        req = self.client.get(url).text
        pass_md = re.findall(r"/pass_md5/[^']*", req)[0]
        token = pass_md.split("/")[-1]
        self.client.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Referer": f"{url}", "Accept-Language": "en-GB,en;q=0.5"})
        drylink = self.client.get(f"{domain}{pass_md}").text
        streamlink = f"{drylink}zUEJeL3mUN?token={token}"
        print(streamlink)
        return streamlink
    
    def streamtape(self, url):
        string = re.findall("""v\/([^"']*)\/""", url)[0]
        request = self.client.get(f"https://streamtape.com/e/{string}").text
        regex = r"""'robotlink'\)\.innerHTML = '(.*?)'\+ \('(.*?)'\)"""
        results = re.findall(regex, request)
        for tuple in results:
            url = tuple[0]
            rest = tuple[1]
        li = f"https:{url}{rest[3:]}"
        return li