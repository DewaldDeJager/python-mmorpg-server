from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network.modules import HealTypes

class HealPacketData(CamelModel):
    instance: str
    type: HealTypes
    amount: int

class HealPacket(Packet):
    def __init__(self, data: HealPacketData):
        super().__init__(id=Packets.Heal, data=data)
