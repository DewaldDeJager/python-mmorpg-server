from typing import List as TList, Dict, Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes

class Position(CamelModel):
    x: int
    y: int

class ListPacketData(CamelModel):
    entities: Optional[TList[str]] = None
    positions: Optional[Dict[str, Position]] = None

class ListPacket(Packet):
    def __init__(self, opcode: Opcodes.List, info: ListPacketData):
        super().__init__(id=Packets.List, opcode=opcode, data=info)
