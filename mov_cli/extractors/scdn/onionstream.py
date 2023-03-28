import httpx
import re


# url = "https://onionstream.live/reddit/cdn.php?id=amazon1-fr.php"
def get_link(url):
    id = url[url.rindex("=") + 1 :]
    link = f"https://onionstream.live/live/{id}"
    r3 = httpx.get(link, headers={"referer": "https://wecast.to//"}).text
    iframe = re.findall("i?frame.+?src=[\"']?([^\"' ]+)", r3, flags=re.IGNORECASE)[0]
    number = re.findall(r"embed/(.*)", iframe)[0]
    og = f"https://wecast.to/onionstream.php?stream={number}"
    cheese = httpx.get(og, headers={"referer": "https://wecast.to//"}).text
    m3u8 = re.findall(r"source:\"(.*?)\"", cheese)[0]
    return m3u8
