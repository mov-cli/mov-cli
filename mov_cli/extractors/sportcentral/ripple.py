import requests
import re

def get_link(url):
    r = requests.get(url).text
    iframe = re.findall(r"iframe src=(.*?) ", r)[0]
    r2 = requests.get(iframe).text
    iframe2 = re.findall(r"iframe src=\"(.*?)\"", r2)[0]
    r3 = requests.get(iframe2, headers={'referer': "https://livetvon.click/"}).text
    m3u8 = re.findall(r"source:'(.*?)'", r3)[1]
    return m3u8

