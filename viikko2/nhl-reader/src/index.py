from rich.table import Table
from rich.console import Console
from player_reader import PlayerReader
from player_stats import PlayerStats


def show_players_table(players, nationality: str, season: str):
    console = Console()

    title = f"Players from {nationality} – season {season}"
    table = Table(title=title)

    table.add_column("Released", justify="left", style="bold")
    table.add_column("Teams", justify="left")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists),
        )

    console.print(table)


def get_user_input():
    """Get season and nationality input from user."""
    season = input("Season (e.g. 2024-25): ").strip()
    nationality = input("Nationality (e.g. FIN): ").strip().upper()
    return season, nationality


def main():
    season, nationality = get_user_input()
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"

    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    show_players_table(players, nationality, season)


if __name__ == "__main__":
    main()
