from __future__ import annotations
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from httpx import Response
    from ..config import Config

from ..media import Media
import re
from ..scrapers import Scraper
import json

class RemoteStream(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://remotestre.am"
        self.imdb_sug = "https://v2.sg.media-imdb.com/suggestion/{}/{}.json"
        self.catalogue = "https://remotestre.am/catalogue?display=plain"
        self.imdb_epi = "https://www.imdb.com/title/{}/episodes/"

        self.__selected: dict = {}
        self.__selections: dict = {}

    def search(self, query: str) -> dict:
        imdb_sug = self.imdb_sug.format(query[0], query)
        imdb = self.get(imdb_sug)
        self.selection = self.__results(imdb)

        return self.selection
        
    def __results(self, response: Response) -> dict:
        js = response.json()["d"]
        catalogue = self.get(self.catalogue)
        self.__selections = json.loads("{}")

        i = 0

        for item in js:
            id = item.get("id", None)
            if id is not None:
                if not id.startswith("tt"):
                    continue
                if id not in catalogue.text:
                    continue
                i += 1

                title = item.get("l")
                qid = item.get("qid")
                if qid == "tvSeries":
                    qid = "show"
                
                img = item.get("i")["imageUrl"]
                    
                year = item.get("yr", None)
                if year is None:
                    year = item.get("y")
                
                js_dict = self.__selections[i] = {}
                js_dict["title"] = title
                js_dict["id"] = id
                js_dict["type"] = qid
                js_dict["img"] = img
                js_dict["year"] = year
        
        return self.__selections
    
    def select(self, selection: int) -> dict:
        self.__selected = self.__selections[selection]
    
    def getMedia(self, season: int = None, episode: int = None) -> Media:
        if self.__selected.get("type") == "show":
            s = self.__tv(season, episode)
        else:
            s = self.__movie()
        
        return s
    
    def getSeasons(self) -> int:
        if self.__selected.get("type") == "movie":
            return None
        
        id = self.__selected.get("id")
        imdb_epi = self.imdb_epi.format(id)
        imdb = self.get(imdb_epi)
        soup = self.soup(imdb.text)
        seasons = len(soup.findAll("li", {"data-testid": "tab-season-entry"}))
        return seasons
    
    def getEpisodes(self, season: int) -> int:
        if self.__selected.get("type") == "movie":
            return None
        
        id = self.__selected.get("id")
        imdb_epi = self.imdb_epi.format(id) + f"?season={season}"
        imdb = self.get(imdb_epi)
        soup = self.soup(imdb.text)
        episodes = len(soup.findAll("article", {"class": "episode-item-wrapper"}))
        return episodes

    def cdn(self, season: int = None, episode: int = None) -> str:
        id = self.__selected.get("id")
        if season:
            url = f"https://remotestre.am/e/?imdb={id}&s={season}&e={episode}"
        else:
            url = f"https://remotestre.am/e/?imdb={id}"
        
        req = self.get(url).text
        file = re.findall('"file":"(.*?)"', req)[0]
        return file

    def __tv(self, season: int, episode: int) -> dict:
        url = self.cdn(season, episode)
        __dict = self.make_json(
            self.__selected.get("title"),
            url,
            "show",
            self.base_url,
            self.__selected.get("img"),
            self.getSeasons(),
            season,
            episode,
            self.__selected.get("year")
        )
        return Media(__dict)

    def __movie(self) -> dict:
        url = self.cdn()
        __dict = self.make_json(
            self.__selected.get("title"),
            url,
            "movie",
            self.base_url,
            self.__selected.get("img"),
            year=self.__selected.get("year")
        )
        return Media(__dict)
