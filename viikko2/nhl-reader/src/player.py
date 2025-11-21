class Player:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.team = data.get("team")
        self.goals = data.get("goals", 0)
        self.assists = data.get("assists", 0)
        self.nationality = data.get("nationality")

    @property
    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name} team {self.team} goals {self.goals} assists {self.assists}"
