from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets

class PointsPacketData(CamelModel):
    instance: str
    hit_points: Optional[int] = None
    max_hit_points: Optional[int] = None
    mana: Optional[int] = None
    max_mana: Optional[int] = None

class PointsPacket(Packet):
    def __init__(self, data: PointsPacketData):
        super().__init__(id=Packets.Points, data=data)
