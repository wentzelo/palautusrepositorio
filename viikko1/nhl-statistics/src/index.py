from player_reader import PlayerReader
from statistics_service import StatisticsService, SortBy

def main():
    stats = StatisticsService(
        PlayerReader("https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt")
    )
    philadelphia_flyers_players = stats.team("PHI")
    top_scorers = stats.top(10)
    top_assists = stats.top(5, SortBy.ASSISTS)

    print("Philadelphia Flyers:")
    for player in philadelphia_flyers_players:
        print(player)

    print()  

    print("Top point getters:")
    for player in top_scorers:
        print(player)

    print("Top assist getters:")
    for player in top_assists:
        print(player)

if __name__ == "__main__":
    main()
