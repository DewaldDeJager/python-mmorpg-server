from typing import List, Optional, Union
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.shared_types import SlotData

class NPCData(CamelModel):
    name: Optional[str] = None
    text: Optional[List[str]] = None
    role: Optional[str] = None
    store: Optional[str] = None

class NPCPacketData(CamelModel):
    instance: Optional[str] = None
    text: Optional[str] = None
    slots: Optional[List[SlotData]] = None

class NPCPacket(Packet):
    def __init__(self, opcode: Opcodes.NPC, data: Union[NPCPacketData, NPCData, None] = None):
        super().__init__(id=Packets.NPC, opcode=opcode, data=data)
