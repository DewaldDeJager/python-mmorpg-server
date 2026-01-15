from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import Interfaces

class InterfacePacketData(CamelModel):
    identifier: Interfaces

class InterfacePacket(Packet):
    def __init__(self, opcode: Opcodes.Interface, data: InterfacePacketData):
        super().__init__(id=Packets.Interface, opcode=opcode, data=data)
