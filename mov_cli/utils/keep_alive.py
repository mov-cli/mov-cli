import time
# import multiprocessing as mp
# import threading

from .httpclient import HttpClient


class KP:
    def __init__(self, website: str, time: int = 120):
        self.client = HttpClient()
        self.time = time
        self.website = website
        # self.cr_th()

    def ping(self, website: str = None, headers: dict = None):
        if not website:
            website = self.website
        while True:
            self.client.set_headers(headers)
            x = self.client.get(website)
            print(x.text)
            time.sleep(self.time)

    # def cr_th(self):
    #    t1 = threading.Thread(target=asyncio.run(self.ping()))
    #    t1.start()

# def main():
#    mp.set_start_method('spawn')
#    x = KP("https://www.google.com", 2)
#    m1 = mp.Process(asyncio.run(x.ping()))
#    m1.start()
#    m1.join()
#    print("hello")
#

# main()
