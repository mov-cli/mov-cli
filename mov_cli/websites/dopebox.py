import json

from .actvid import Actvid
from bs4 import BeautifulSoup as BS


class DopeBox(Actvid):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url
        self.rep_key = "6LeWLCYeAAAAAL1caYzkrIY-M59Vu41vIblXQZ48"
        # self.redo()

    """def cdn_url(self, rabbid, rose, num):
        self.client.set_headers({"X-Requested-With": "XMLHttpRequest"})
        # data = json.loads(self.client.get(
        #    f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbid}&_token={rose}&_number={num}"))['sources'][0][
        #    'file']
        data = json.loads(
            self.client.get(
                f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbid}&_token={rose}&_number={num}"
            ).text
        )["sources"][0]["file"]
        return data"""

    def ask(self, series_id):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, "html.parser").select(".dropdown-item")
        ]
        season = input(
            self.lmagenta(
                f"Please input the season number(total seasons:{len(season_ids)}): "
            )
        )
        rf = self.client.get(
            f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        )
        episodes = [i["data-id"] for i in BS(rf, "html.parser").select(".episode-item")]
        episode = episodes[
            int(
                input(
                    self.lmagenta(
                        f"Please input the episode number(total episodes in season:{season}):{len(episodes)} : "
                    )
                )
            )
            - 1
        ]
        ep = self.getep(f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}", data_id=episode)
        return episode, season, ep

    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text
        soup = BS(source, "html.parser")

        unformated = soup.find("div", {"data-id": f"{data_id}"})

        children = unformated.findChildren("div", {"class": "episode-number"})
        for child in children:
            text = child.text

        text = text.split("Episode")[1]
        text = text.split(":")[0]

        return text

    def server_id(self, mov_id):
        rem = self.client.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = BS(rem, "html.parser")
        return [i["data-id"] for i in soup.select(".link-item")][0]

    def ep_server_id(self, ep_id):
        rem = self.client.get(
            f"{self.base_url}/ajax/v2/episode/servers/{ep_id}/#servers-list"
        )
        soup = BS(rem, "html.parser")
        return [i["data-id"] for i in soup.select(".link-item")][0]
