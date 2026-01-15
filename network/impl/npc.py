from typing import List, Optional, Union
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.shared_types import SlotData

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
