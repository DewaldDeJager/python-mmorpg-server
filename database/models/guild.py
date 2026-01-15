from typing import List
from packages.server_python.network.model import CamelModel
from packages.server_python.network.impl.guild import Decoration, Member

class GuildModel(CamelModel):
    identifier: str
    name: str
    creation_date: int
    owner: str
    invite_only: bool
    experience: int
    decoration: Decoration
    members: List[Member]
