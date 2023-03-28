import httpx
import re


def get_link(url):
    r = httpx.get(url).text
    php = re.findall(r"src=\"(.*?) sc", r)[0]
    r_php = httpx.get(php).text
    m3u8 = re.findall(r"source: '(.*?)'", r_php)[0]
    return m3u8
