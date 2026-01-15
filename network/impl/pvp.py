from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets

class PVPPacketData(CamelModel):
    state: bool

class PVPPacket(Packet):
    def __init__(self, data: PVPPacketData):
        super().__init__(id=Packets.PVP, data=data)
