import re
import httpx
from ..utils.props import SelectedNotAvailable


def dood(url):
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    video_id = httpx.URL(url).path.split("/")[-1]
    print(video_id)
    webpage_html = httpx.get(
        f"https://dood.to/e/{video_id}", headers=headers, follow_redirects=True
    )
    webpage_html = webpage_html.text
    try:
        pass_md5 = re.search(r"/pass_md5/[^']*", webpage_html).group()
    except:
        raise SelectedNotAvailable
    urlh = f"https://dood.to{pass_md5}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
        "referer": "https://dood.to",
    }
    res = httpx.get(urlh, headers=headers).text
    md5 = pass_md5.split("/")
    true_url = res + "MovCli3oPi?token=" + md5[-1]
    return true_url
