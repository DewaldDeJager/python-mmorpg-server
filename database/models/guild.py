from typing import List
from network.model import CamelModel
from network.impl.guild import Decoration, Member

class GuildModel(CamelModel):
    identifier: str
    name: str
    creation_date: int
    owner: str
    invite_only: bool
    experience: int
    decoration: Decoration
    members: List[Member]
