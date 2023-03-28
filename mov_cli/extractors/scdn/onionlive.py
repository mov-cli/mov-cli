import httpx

url = "https://onionstream.live/channeltv/us-espn.php}"
x = (
    "{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/102.0.0.0 Safari/537.36'} "
)
# x = "{'User-Agent': Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0
# Safari/537.36'}"


def get_link(url):
    # id = url[url.rindex('=') + 1:]
    # r3 = httpx.get(url, ).text
    r3 = httpx.get(url, headers={"referer": x}).text

    return r3
    # iframe = re.findall('i?frame.+?src=[\"\']?([^\"\' ]+)', r3, flags=re.IGNORECASE)[0]
    # number = re.findall(r"embed/(.*)", iframe)[0]
    # og = f"https://wecast.to/onionstream.php?stream={number}"
    # cheese = httpx.get(og, headers={'referer': "https://wecast.to//"}).text
    # m3u8 = re.findall(r"source:\"(.*?)\"", cheese)[0]
    # return m3u8


print(get_link(url))
