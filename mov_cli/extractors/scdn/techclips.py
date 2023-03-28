import re
import httpx


def get_link(url):
    r = httpx.get(url).text
    iframe = re.findall(r'iframe src="(.+?)"', r)[0]
    r_iframe = httpx.get(iframe).text
    servers = eval(re.findall(r"var servs = (\[.+?\]);", r_iframe)[0])
    stream_id = re.findall(r"source: 'https://' \+ serv \+ '(.*?)'", r_iframe)[0]
    for server in servers:
        m3u8 = "https://" + server + stream_id
    return m3u8
