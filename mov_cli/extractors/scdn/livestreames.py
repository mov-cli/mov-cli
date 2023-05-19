import httpx
import re
from bs4 import BeautifulSoup as BS


def get_link(url):
    req = httpx.get(url).text
    soup = BS(req, "html.parser")
    iframe = soup.find("iframe", {"class": "video"}).get("src")
    iframe1 = httpx.get(iframe).text
    soup = BS(iframe1, "html.parser")
    iframe = soup.find("iframe", {"id": "thatframe"}).get("src")
    iframe2 = httpx.get(iframe).text
    m3u8 = re.findall(r"source: \"(.*?)\"", iframe2)[0]
    return m3u8
