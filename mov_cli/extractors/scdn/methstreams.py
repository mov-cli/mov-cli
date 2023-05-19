import httpx
import re
from bs4 import BeautifulSoup


def get_link(url):
    video_html = httpx.get(url).text
    video = BeautifulSoup(video_html, self.parser)
    iframe = video.find("iframe").get("src")
    r_iframe = httpx.get(iframe).text
    m3u8 = re.findall(r"source: \"(.*?)\"", r_iframe)[0]
    return m3u8
