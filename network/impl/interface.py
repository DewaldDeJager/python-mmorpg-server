from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.modules import Interfaces

class InterfacePacketData(CamelModel):
    identifier: Interfaces

class InterfacePacket(Packet):
    def __init__(self, opcode: Opcodes.Interface, data: InterfacePacketData):
        super().__init__(id=Packets.Interface, opcode=opcode, data=data)
