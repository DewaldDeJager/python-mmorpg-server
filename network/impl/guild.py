from typing import List, Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.modules import GuildRank, BannerColour, BannerOutline, BannerCrests

class Member(CamelModel):
    username: str
    rank: Optional[GuildRank] = None
    join_date: Optional[int] = None
    server_id: Optional[int] = None  # -1 if offline

class Decoration(CamelModel):
    banner: BannerColour
    outline: BannerOutline
    outline_colour: BannerColour
    crest: BannerCrests

# Contains only necessary information to be passed to client.
class ListInfo(CamelModel):
    name: str
    members: int
    decoration: Decoration

class GuildData(CamelModel):
    identifier: str
    name: str
    creation_date: int
    owner: str
    invite_only: bool
    experience: int
    decoration: Decoration
    members: List[Member]

# Used to relay update information to other players.
class UpdateInfo(CamelModel):
    opcode: Opcodes.Guild
    username: str
    server_id: Optional[int] = None
    rank: Optional[GuildRank] = None

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
