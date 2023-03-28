import re
import httpx


def get_link(url):
    r = httpx.get(url).text
    m3u8 = re.findall(r"source src=\"(.+?)\"", r)[0]
    return m3u8
