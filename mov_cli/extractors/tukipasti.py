import httpx
import re

def tukipasti(html):
    regex = r'''"https:\/\/tukipasti\.com(.*?)"'''
    s = re.findall(regex, html)[0]
    req = httpx.get(f"https://tukipasti.com{s}").text
    url = re.findall("var urlPlay = '(.*?)'", req)[0]
    return url, f"https://tukipasti.com{s}"
