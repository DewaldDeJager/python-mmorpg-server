from network.packet import Packet
from network.packets import Packets

PoisonPacketData = int

class PoisonPacket(Packet):
    def __init__(self, type: int):
        super().__init__(id=Packets.Poison, data=type)
