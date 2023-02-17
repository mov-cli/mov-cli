import re
import requests
def get_link(url):
    r = requests.get(url).text
    m3u8 = re.findall(r"source src=\"(.+?)\"", r)[0]
    return m3u8
