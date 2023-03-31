import sys

import httpx

default_header: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.163 "
    "Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.5",
}


class HttpClient:
    def __init__(self, headers: dict = None, cookies: dict = None):
        if headers is None:
            headers = default_header
        self.session = httpx.Client(timeout=10.0, headers=headers, cookies=cookies)

    def get(self, page: str, redirects: bool = False) -> httpx.Response:
        print(page)
        try:
            req = self.session.get(page, follow_redirects=redirects)
            self.session.headers["Referer"] = page
        except Exception as e:
            print(
                f"Error: {e}",
                "\n Please open an issue if this is not due due to your internet connection",
            )
            sys.exit(-1)
        return req

    def post(self, page: str, data: dict = None, json=None) -> httpx.Response:
        print(page)
        if json is None:
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
        else:
            try:
                req = self.session.post(page, json=json)
                self.session.headers["Referer"] = page
            except Exception as e:
                print(
                    f"Error: {e}",
                    "\n Please open an issue if this is not due due to your internet connection",
                )
                sys.exit(-1)
            return req

    def head(self, page: str, redirects: False) -> httpx.Response:
        print(page)
        try:
            req = self.session.head(page, follow_redirects=redirects)
            self.session.headers["Referer"] = page
        except Exception as e:
            print(
                f"Error: {e}",
                "\n Please open an issue if this is not due due to your internet connection",
            )
            sys.exit(-1)
        return req

    def set_headers(self, header: dict) -> None:
        self.session.headers = header
        # do not use this!w

    def set_cookies(self, cookies: dict) -> None:
        self.session.cookies = cookies

    def add_elem(self, elements: dict) -> None:
        for i in elements.items():
            self.session.headers[i[0]] = i[1]
