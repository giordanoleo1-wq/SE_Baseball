from dataclasses import dataclass
@dataclass
class Team:
    id: str
    year: int
    team_code: str
    name: str


    def __str__(self):
        return f"{self.id} - {self.year} - {self.team_code}"
    def __hash__(self):
        return hash(self.id)
