from enum import Enum
from player_reader import PlayerReader

class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3

class StatisticsService:
    def __init__(self, reader):
        self._players = reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name):
        players_of_team = filter(
            lambda player: player.team == team_name,
            self._players
        )

        return list(players_of_team)

    def top(self, how_many, sort_by=SortBy.POINTS):
        if sort_by == SortBy.POINTS:
            key = lambda player: player.points
        elif sort_by == SortBy.GOALS:
            key = lambda player: player.goals
        else:
            key = lambda player: player.assists

        sorted_players = sorted(
            self._players,
            reverse=True,
            key=key
        )

        result = []
        i = 0
        while i <= how_many and i < len(sorted_players):
            result.append(sorted_players[i])
            i += 1

        return result