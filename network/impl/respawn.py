from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets

class RespawnPacketData(CamelModel):
    x: int
    y: int

class RespawnPacket(Packet):
    def __init__(self, data: RespawnPacketData):
        super().__init__(id=Packets.Respawn, data=data)
