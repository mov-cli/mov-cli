import requests


class Subtitles:
    """
    pull subtitles from api.opensubtitles.com and return
    a link to the .srt file which can be passed into vlc or mpv
    """

    def __init__(self, language="en"):
        self.language = language
        self.base_url = "https://api.opensubtitles.com/api/v1"
        self.get_headers = {
            "User-Agent": "movcli",
            "Api-Key": "bN8yCgz49NpcZOA7ImHbXdklQVc3UMRJ",
        }

    def get_tv_subs(self, name, episode_number, season_number) -> str:
        url_params = f"/subtitles/?query={name}&languages={self.language}&episode_number={episode_number}&season_number={season_number}"
        response = requests.get(self.base_url + url_params, headers=self.get_headers)
        return self.__get_link(response.json()["data"][0]['attributes']['files'][0]['file_id'])

    def get_movie_subs(self, name) -> str:
        url_params = f"/subtitle/?query={name}&languages={self.language}"
        response = requests.get(self.base_url + url_params, headers=self.get_headers)
        return self.__get_link(response.json()["data"][0]['attributes']['files'][0]['file_id'])

    def __get_link(self, id) -> str:
        headers = {
            "User-Agent": "movcli",
            "Api-Key": "bN8yCgz49NpcZOA7ImHbXdklQVc3UMRJ",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {"file_id": f"{id}"}

        response = requests.post(self.base_url + "/download", json=payload, headers=headers)
        return response.json()['link']

subtitles = Subtitles("en")
print(subtitles.get_tv_subs("community", 4, 1))
