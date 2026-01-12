from dataclasses import dataclass
@dataclass
class Appearence:
    id : int
    year : int
    team_code: str
    team_id: int
    player_id: str

    def __str__(self):
        return f'{self.team_code} {self.player_id}'
    def __hash__(self):
        return hash(self.id)