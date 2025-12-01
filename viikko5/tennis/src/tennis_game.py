class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_points += 1
        else:
            self.player2_points += 1

    def get_score(self):
        if self._is_tie():
            return self._tie_score()

        if self._has_advantage_or_win():
            return self._advantage_or_win_score()

        return self._regular_score()

    def _is_tie(self):
        return self.player1_points == self.player2_points

    def _tie_score(self):
        if self.player1_points < 3:
            return f"{self.SCORE_NAMES[self.player1_points]}-All"
        return "Deuce"

    def _has_advantage_or_win(self):
        return self.player1_points >= 4 or self.player2_points >= 4

    def _advantage_or_win_score(self):
        diff = self.player1_points - self.player2_points

        if diff == 1:
            return f"Advantage {self.player1_name}"
        elif diff == -1:
            return f"Advantage {self.player2_name}"
        elif diff >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"

    def _regular_score(self):
        p1 = self.SCORE_NAMES[self.player1_points]
        p2 = self.SCORE_NAMES[self.player2_points]
        return f"{p1}-{p2}"
