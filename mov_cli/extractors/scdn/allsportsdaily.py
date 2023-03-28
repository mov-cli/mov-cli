import httpx
import re


def get_link(url):
    r = httpx.get(url).text
    print(r)
    m3u8 = re.findall(r"source\s*:\s+?(?:\"|')(.+?)(?:\"|')", r)[0]
    return m3u8
