import re
import httpx

url = "http://rainostreams.com/nba/thunder/?moment=8221012023"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93
# Safari/537.36"
domain = "rainostreams.com"


def get_link(url):
    if "?moment" in url:
        url = url.split("/?moment")[0]
        url = (
            url.replace("https", "http").replace(domain, "bdnewszh.com/embed") + ".php"
        )
        r = httpx.get(url, headers={"referer": "https://rainostreams.com/"}).text
        m3u8 = re.findall(r"source: '(.*?)'", r)[0][2:]
        m3u8 = "http://" + m3u8
        return m3u8
