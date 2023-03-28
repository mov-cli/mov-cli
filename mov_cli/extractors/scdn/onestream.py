import httpx
import re
import random
import base64


def get_link(url):
    r = httpx.get(url).text
    token = re.findall(r'\"_token\": \"(.+)"', r)[0]
    sport = re.findall(r"sport: '(.+)'", r)[0]
    id = str(url).split("/")[-1].split("?")[0]
    math = str(round(random.random() * 64))
    r = httpx.post(
        f"https://1stream.eu/getspurcename?{id}={math}",
        data={"eventId": id, "_token": token, "sport": sport},
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "Origin": "https://1stream.eu",
            "Referer": url,
            "x-requested-with": "XMLHttpRequest",
        },
    ).json()
    print(r["source"])
    m3u8 = base64.b64decode(r["source"]).decode("utf-8")
    return m3u8
