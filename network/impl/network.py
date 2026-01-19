from typing import Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes

class NetworkPacketData(CamelModel):
    timestamp: Optional[int] = None

class NetworkPacket(Packet):
    def __init__(self, opcode: Opcodes.Network, data: Optional[NetworkPacketData] = None):
        super().__init__(id=Packets.Network, opcode=opcode, data=data)
