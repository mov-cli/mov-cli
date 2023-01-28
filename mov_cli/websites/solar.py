from .actvid import Actvid
from bs4 import BeautifulSoup as BS


class Solar(Actvid):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.rep_key = "6LeWLCYeAAAAAL1caYzkrIY-M59Vu41vIblXQZ48"
        self.redo()

    def ask(self, series_id):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "lxml").select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        rf = self.client.get(
            f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        )
        episodes = [i["data-id"] for i in BS(rf, "lxml").select(".eps-item")]
        episode = episodes[
            int(self.askepisode(len(episodes))) - 1
        ]
        ep = self.getep(f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}", episode)
        return episode, season, ep

    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text

        soup = BS(source, "lxml")

        unformated = soup.find("a", {"data-id": f"{data_id}"})['title']

        formated = unformated.split("Eps")[1]
        formated = formated.split(":")[0]

        return formated

"""    def cdn_url(self, rabbid, rose, num) -> str:
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        data = self.client.get(
            f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbid}&_token={rose}&_number={num}"
        ).json()["sources"][0]["file"]
        return data
"""