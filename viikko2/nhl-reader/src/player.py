class Player:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.team = data.get("team")
        self.goals = data.get("goals", 0)
        self.assists = data.get("assists", 0)
        self.nationality = data.get("nationality")

    def __str__(self):
        total = self.goals + self.assists
        return (f"{self.name:20} {self.team:15} "
                f"{self.goals:2} + {self.assists:2} = {total}")
