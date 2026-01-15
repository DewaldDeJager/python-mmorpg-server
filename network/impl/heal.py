from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network.modules import HealTypes

class HealPacketData(CamelModel):
    instance: str
    type: HealTypes
    amount: int

class HealPacket(Packet):
    def __init__(self, data: HealPacketData):
        super().__init__(id=Packets.Heal, data=data)
