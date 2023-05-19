import re
import httpx
from utils import jsunpack


def get_link(url):
    r = httpx.get(url).text
    iframe = re.findall(r"iframe src=\"(.*?)\"", r)[0]
    r2 = httpx.get(iframe).text
    iframe2 = re.findall(r"iframe src=\"(.*?)\"", r2)[0]
    r3 = httpx.get(iframe2, headers={"referer": "https://sportsembed.su/"}).text
    re_js = jsunpack.unpack(
        re.compile(r"(eval\(function\(p,a,c,k,e,d\).+?{}\)\))").findall(r3)[0]
    )
    m3u8 = re.findall(r"src=\"(.*?)\"", re_js)[0]
    # soup = BeautifulSoup(r, 'self.scraper')
    # iframe = soup.iframe
    # src = iframe['src']
    # r_src = httpx.get(src).text
    # fid = re.findall(r"t>fid='(.*?)'", r_src)[0]
    # n = re.findall(r"embed(.*?).j", r_src)[0]
    # php = f"https://vikistream.com/embed{n}.php?player=desktop&live={fid}"
    # r_php = httpx.get(php).text
    # expand = re.findall(r"n\((.*?).join", r_php)[0]
    # lis = json.loads(expand)
    # m3u8 = "".join(lis)
    return m3u8
