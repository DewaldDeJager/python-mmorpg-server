from typing import Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes

class EnchantPacketData(CamelModel):
    index: int
    is_shard: Optional[bool] = None

class EnchantPacket(Packet):
    def __init__(self, opcode: Opcodes.Enchant, data: EnchantPacketData):
        super().__init__(id=Packets.Enchant, opcode=opcode, data=data)
