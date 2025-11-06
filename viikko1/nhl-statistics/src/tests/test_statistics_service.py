#Github Copilotilla tuotettu

import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]


class TestStatisticsService(unittest.TestCase):

    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_right_player(self):
        player = self.stats.search("Gretzky")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.points, 124)

    def test_search_returns_none_if_no_match(self):
        player = self.stats.search("Nonexistent")
        self.assertIsNone(player)

    def test_team_filters_by_team(self):
        edmonton_players = self.stats.team("EDM")
        names = [p.name for p in edmonton_players]
        self.assertListEqual(
            names,
            ["Semenko", "Kurri", "Gretzky"]
        )

    def test_team_empty_if_team_not_found(self):
        players = self.stats.team("XYZ")
        self.assertEqual(players, [])

    def test_top_returns_correct_number_of_players(self):
        top_three = self.stats.top(2)
        self.assertEqual(len(top_three), 3)
        self.assertEqual(top_three[0].name, "Gretzky")
        self.assertEqual(top_three[1].name, "Lemieux")
        self.assertEqual(top_three[2].name, "Yzerman")

    def test_top_bounds(self):

        top_players = self.stats.top(20)

        self.assertEqual(len(top_players), 5)

    def test_top_sorted_by_goals(self):
        top = self.stats.top(2, sort_by=SortBy.GOALS)
        self.assertEqual(top[0].name, "Lemieux")
        self.assertEqual(top[1].name, "Yzerman")

    def test_top_sorted_by_assists(self):
        top = self.stats.top(2, sort_by=SortBy.ASSISTS)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[1].name, "Yzerman")

    def test_top_default_sort_is_points(self):
        top_default = self.stats.top(2)
        top_points = self.stats.top(2, sort_by=SortBy.POINTS)
        self.assertEqual(
            [p.name for p in top_default],
            [p.name for p in top_points]
        )

if __name__ == '__main__':
    unittest.main()
