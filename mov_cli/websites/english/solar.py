from .actvid import Provider as pv
from bs4 import BeautifulSoup as BS


class Provider(pv):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.dseasonp = True
        self.dshowp = True

    def ask(self, series_id):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        rf = self.client.get(
            f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        )
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".eps-item")]
        ep = self.askepisode(len(episodes))
        episode = episodes[int(ep) - 1]
        return episode, season, ep

    def get_link(self, thing_id: str) -> tuple:
        req = self.client.get(f"{self.base_url}/ajax/sources/{thing_id}").json()["link"]
        print(req)
        return req, self.rabbit_id(req)
