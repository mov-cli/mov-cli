import re
import httpx
from urllib.parse import urlparse, quote
import json


def get_link(url: str) -> str:
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
        "Safari/537.36 "
    )
    base_url = "http://" + urlparse(url).netloc
    r_game = httpx.get(url).text
    re_vidgstream = re.compile(r'var vidgstream = "(.+?)";').findall(r_game)[0]
    if base_url == "http://liveonscore.tv":
        re_gethlsUrl = re.compile(r"gethlsUrl\(vidgstream, (.+?), (.+?)\);").findall(
            r_game
        )[0]
        r_hls = httpx.get(
            base_url
            + "/gethls.php?idgstream=%s&serverid=%s&cid=%s"
            % (quote(re_vidgstream, safe=""), re_gethlsUrl[0], re_gethlsUrl[1]),
            headers={
                "User-Agent": user_agent,
                "Referer": url,
                "X-Requested-With": "XMLHttpRequest",
            },
        ).text
    else:
        r_hls = httpx.get(
            base_url + "/gethls.php?idgstream=%s" % quote(re_vidgstream, safe=""),
            headers={
                "User-Agent": user_agent,
                "Referer": url,
                "X-Requested-With": "XMLHttpRequest",
            },
        ).text
    json_hls = json.loads(r_hls)
    m3u8 = json_hls["rawUrl"]
    return m3u8
