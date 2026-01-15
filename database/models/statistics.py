from typing import Dict, List
from packages.server_python.network.model import CamelModel

class StatisticsData(CamelModel):
    pvp_kills: int
    pvp_deaths: int
    mob_kills: Dict[str, int]
    mob_examines: List[str]
    resources: Dict[str, int]
    drops: Dict[str, int]

    creation_time: int
    total_time_played: int
    average_time_played: int
    last_login: int
    login_count: int

    cheater: bool

class PlayerStatisticsModel(StatisticsData):
    username: str
