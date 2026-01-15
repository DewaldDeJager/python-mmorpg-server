from typing import List, Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.shared_types import SlotData

class LootBagPacketData(CamelModel):
    items: Optional[List[SlotData]] = None
    index: Optional[int] = None

class LootBagPacket(Packet):
    def __init__(self, opcode: Opcodes.LootBag, info: LootBagPacketData):
        super().__init__(id=Packets.LootBag, opcode=opcode, data=info)
