from typing import List, Literal, Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets

class ClientHandshakePacketData(CamelModel):
    type: Literal['client']
    instance: Optional[str] = None # Player's instance.
    server_id: Optional[int] = None
    server_time: Optional[int] = None

class HubHandshakePacketData(CamelModel):
    type: Literal['hub']
    g_ver: str # Game version.
    name: str
    server_id: int
    access_token: str # Denied if mismatches
    remote_host: str # Relayed to game clients as the server's IP.
    port: int
    players: List[str]
    max_players: int

class AdminHandshakePacketData(CamelModel):
    type: Literal['admin']
    access_token: str

HandshakePacketData = Union[ClientHandshakePacketData, HubHandshakePacketData, AdminHandshakePacketData]

class HandshakePacket(Packet):
    def __init__(self, data: HandshakePacketData):
        super().__init__(id=Packets.Handshake, data=data)
