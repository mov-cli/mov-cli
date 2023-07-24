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
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".episode-item")]
        episode = episodes[int(self.askepisode(len(episodes))) - 1]
        ep = self.getep(
            f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}",
            data_id=episode,
        )
        return episode, season, ep

    def getep(self, url, data_id):
        source = self.client.get(f"{url}").text
        soup = BS(source, self.scraper)

        unformated = soup.find("div", {"data-id": f"{data_id}"})

        children = unformated.findChildren("div", {"class": "episode-number"})
        for child in children:
            text = child.text

        text = text.split("Episode")[1]
        text = text.split(":")[0]

        return text

    def server_id(self, mov_id):
        rem = self.client.get(f"{self.base_url}/ajax/movie/episodes/{mov_id}")
        soup = BS(rem, self.scraper)
        return [i["data-id"] for i in soup.select(".link-item")][0]

    def get_link(self, thing_id: str) -> tuple:
        req = self.client.get(f"{self.base_url}/ajax/sources/{thing_id}").json()[
            "link"
        ]
        print(req)
        return req, self.rabbit_id(req)

    def ep_server_id(self, ep_id):
        rem = self.client.get(
            f"{self.base_url}/ajax/v2/episode/servers/{ep_id}/#servers-list"
        )
        soup = BS(rem, self.scraper)
        return [i["data-id"] for i in soup.select(".link-item")][0]

    def ds(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        season = self.askseason(len(season_ids))
        rf = self.client.get(
            f"{self.base_url}/ajax/v2/season/episodes/{season_ids[int(season) - 1]}"
        )
        episodes = [i["data-id"] for i in BS(rf, self.scraper).select(".episode-item")]
        for e in range(len(episodes)):
            episode = episodes[e]
            sid = self.ep_server_id(episode)
            iframe_url, tv_id = self.get_link(sid)
            iframe_link, iframe_id = self.rabbit_id(iframe_url)
            url = self.cdn_url(iframe_link, iframe_id)
            self.dl(url, name, season=season, episode=e + 1)

    def sd(self, series_id: str, name):
        r = self.client.get(f"{self.base_url}/ajax/v2/tv/seasons/{series_id}")
        season_ids = [
            i["data-id"] for i in BS(r, self.scraper).select(".dropdown-item")
        ]
        for s in range(len(season_ids)):
            rf = self.client.get(
                f"{self.base_url}/ajax/v2/season/episodes/{season_ids[s]}"
            )
            episodes = [
                i["data-id"] for i in BS(rf, self.scraper).select(".episode-item")
            ]
            for e in range(len(episodes)):
                episode = episodes[e]
                sid = self.ep_server_id(episode)
                iframe_url, tv_id = self.get_link(sid)
                iframe_link, iframe_id = self.rabbit_id(iframe_url)
                url = self.cdn_url(iframe_link, iframe_id)
                self.dl(url, name, season=s + 1, episode=e + 1)
