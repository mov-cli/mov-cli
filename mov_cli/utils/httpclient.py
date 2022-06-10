import sys

import httpx

default_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.163 "
    "Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.5",
}


class HttpClient:
    def __init__(self, headers=default_header):
        self.session = httpx.Client(timeout=10.0, headers=headers)

    def get(self, page):
        print(page)
        try:
            req = self.session.get(page)
            self.session.headers["Referer"] = page
        except Exception as e:
            print(
                f"Error: {e}",
                "\n Please open an issue if this is not due due to your internet connection",
            )
            sys.exit(-1)
        return req

    def post(self, page, data):
        try:
            req = self.session.post(page, data=data)
            self.session.headers["Referer"] = page
        except Exception as e:
            print(
                f"Error: {e}",
                "\n Please open an issue if this is not due due to your internet connection",
            )
            sys.exit(-1)
        return req

    def set_headers(self, header):
        self.session.headers = header

    def add_elem(self, key, value):
        self.session.headers[key] = value
