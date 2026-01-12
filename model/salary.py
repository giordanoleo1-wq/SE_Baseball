from dataclasses import dataclass
@dataclass
class Salary:
    id : int
    year: int
    team_code: str
    team_id: int
    player_id: str
    salary: float

    def __hash__(self):
        return hash(self.id)