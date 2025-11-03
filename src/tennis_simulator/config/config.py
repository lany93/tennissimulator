from pydantic import BaseModel


class TennisScoring(BaseModel):
    love: str
    fiveen: str
    thirty: str
    forty: str


class Simulation(BaseModel):
    max_players: float
    match_duration_minutes: float
    court_type: str


class Config(BaseModel):
    tennis_score: TennisScoring
    simulation_parameters: Simulation
