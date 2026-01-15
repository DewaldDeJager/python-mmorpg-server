from typing import List, Optional, Dict
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import Skills

class CraftingItemPreview(CamelModel):
    key: str
    level: int

class CraftingRequirement(CamelModel):
    key: str
    count: int
    name: Optional[str] = None

class CraftingResult(CamelModel):
    count: int

class CraftingItem(CamelModel):
    level: int
    experience: int
    chance: Optional[int] = None
    requirements: List[CraftingRequirement]
    result: CraftingResult

class CraftingInfo(CamelModel):
    pass

class CraftingPacketData(CamelModel):
    type: Optional[Skills] = None
    previews: Optional[List[CraftingItemPreview]] = None
    key: Optional[str] = None
    name: Optional[str] = None
    level: Optional[int] = None
    requirements: Optional[List[CraftingRequirement]] = None
    result: Optional[int] = None

class CraftingPacket(Packet):
    def __init__(self, opcode: Opcodes.Crafting, data: CraftingPacketData):
        super().__init__(id=Packets.Crafting, opcode=opcode, data=data)
