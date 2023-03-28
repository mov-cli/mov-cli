import httpx
import re


def get_link(url):
    url = url + "/"
    channel = re.findall(r"ch(.*?)/", url)[0]
    php = f"https://enjoyhd.xyz/hd/live{channel}.php"
    r = httpx.get(php).text
    m3u8 = re.findall(r"source: '(.*?)'", r)[0]
    return m3u8
