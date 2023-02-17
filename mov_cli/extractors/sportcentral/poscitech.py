import requests
import re
from bs4 import BeautifulSoup
def get_link(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    iframe = soup.iframe
    iframe = iframe['src']
    r2 = requests.get(iframe).text
    click = re.findall('i?frame.+?src=[\"\']?([^\"\' ]+)', r2, flags=re.IGNORECASE)[1]
    r3 = requests.get(click, headers={'referer': "https://livetvon.click/"}).text
    m3u8 = re.findall(r"source:'(.*?)'", r3)[1]
    return m3u8
