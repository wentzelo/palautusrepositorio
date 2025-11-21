import requests
from player import Player


class PlayerReader:
    def __init__(self, url: str):
        self._url = url

    def get_players(self):
        response = requests.get(self._url).json()
        return [Player(p) for p in response]