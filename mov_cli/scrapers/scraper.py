import httpx

DEFAULT_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

__all__ = ("Scraper",)

class Scraper():
    def __init__(self, base_url: str) -> None:
        """Anything HTTP/HTTPS related for mov-cli"""   
        self.http = httpx.Client(timeout=15.0, headers=DEFAULT_HEADERS, cookies=None)
        self.base_url = base_url

    def get(self, url: str, redirect: bool = False) -> httpx.Response:
        """Makes a GET request and returns httpx.Response"""
        self.http.headers["Referer"] = url

        get = self.http.get(url, follow_redirects=redirect)

        return get

    def post(self, url: str, data: dict = None, json: dict = None) -> httpx.Response:
        """Makes a POST request and returns httpx.Response"""
        self.http.headers["Referer"] = url

        post = self.http.post(url, data=data, json=json)

        return post

    def set_header(self, header: dict) -> None:
        """
        Able to set custom headers
        
        Not recommended
        """
        self.http.headers = header

    def add_header_elem(self, header_elem: dict) -> None:
        """Add header elements to default header."""
        for elem in header_elem:
            self.http.headers[elem[0]] = elem[1]

    def set_cookies(self, cookies: dict) -> None:
        """Sets cookies."""
        self.http.cookies = cookies

    def search(self, query: str) -> httpx.Response:
        """Search anything. Returns httpx.Response"""
        ...

    def results(self, response: httpx.Response) -> list:
        """Processes Search. Returns list"""
        ...

    def movie(self, items: list) -> dict:
        """When a movie is selected, this will process it. Returns dict"""
        ...

    def tv(self, items: list) -> dict:
        """When a show is selected, this will process it. Returns dict"""
        ...