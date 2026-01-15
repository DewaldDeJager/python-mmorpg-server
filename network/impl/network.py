from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class NetworkPacketData(CamelModel):
    timestamp: Optional[int] = None

class NetworkPacket(Packet):
    def __init__(self, opcode: Opcodes.Network, data: Optional[NetworkPacketData] = None):
        super().__init__(id=Packets.Network, opcode=opcode, data=data)
