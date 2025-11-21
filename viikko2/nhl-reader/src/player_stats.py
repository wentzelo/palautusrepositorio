class PlayerStats:
    def __init__(self, reader):
        # Haetaan kaikki pelaajat kerralla
        self._players = reader.get_players()

    def top_scorers_by_nationality(self, nationality: str):
        # Suodatetaan kansalaisuuden mukaan
        players = [p for p in self._players if p.nationality == nationality]

        # Järjestetään pisteiden mukaan (goals + assists), suurin ensin
        players_sorted = sorted(
            players,
            key=lambda p: p.goals + p.assists,
            reverse=True
        )

        return players_sorted
