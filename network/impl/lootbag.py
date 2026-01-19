from typing import List, Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.shared_types import SlotData

class LootBagPacketData(CamelModel):
    items: Optional[List[SlotData]] = None
    index: Optional[int] = None

class LootBagPacket(Packet):
    def __init__(self, opcode: Opcodes.LootBag, info: LootBagPacketData):
        super().__init__(id=Packets.LootBag, opcode=opcode, data=info)
