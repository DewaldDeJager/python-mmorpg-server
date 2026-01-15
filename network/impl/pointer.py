from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class PointerData(CamelModel):
    type: int
    x: Optional[int] = None
    y: Optional[int] = None
    instance: Optional[str] = None
    button: Optional[str] = None

class PointerPacketData(CamelModel):
    instance: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None
    button: Optional[str] = None

class PointerPacket(Packet):
    def __init__(self, opcode: Opcodes.Pointer, data: Optional[PointerPacketData] = None):
        super().__init__(id=Packets.Pointer, opcode=opcode, data=data)
