import requests
import re

def get_link(url):
    r = requests.get(url).text
    m3u8 = re.findall(r"source\s*:\s+?(?:\"|')(.+?)(?:\"|')", r)[0]
    return m3u8

