from typing import List, Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import GuildRank, BannerColour, BannerOutline, BannerCrests

class Member(CamelModel):
    username: str
    rank: Optional[GuildRank] = None
    join_date: Optional[int] = None
    server_id: Optional[int] = None

class Decoration(CamelModel):
    banner: BannerColour
    outline: BannerOutline
    outline_colour: BannerColour
    crest: BannerCrests

class ListInfo(CamelModel):
    name: str
    members: int
    decoration: Decoration

class GuildPacketData(CamelModel):
    identifier: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    usernames: Optional[List[str]] = None
    server_id: Optional[int] = None
    member: Optional[Member] = None
    members: Optional[List[Member]] = None
    total: Optional[int] = None
    guilds: Optional[List[ListInfo]] = None
    message: Optional[str] = None
    owner: Optional[str] = None
    decoration: Optional[Decoration] = None
    experience: Optional[int] = None
    rank: Optional[GuildRank] = None

class GuildPacket(Packet):
    def __init__(self, opcode: Optional[Opcodes.Guild] = None, data: Optional[GuildPacketData] = None):
        super().__init__(id=Packets.Guild, opcode=opcode, data=data)
