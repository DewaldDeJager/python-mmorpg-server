from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class EnchantPacketData(CamelModel):
    index: int
    is_shard: Optional[bool] = None

class EnchantPacket(Packet):
    def __init__(self, opcode: Opcodes.Enchant, data: EnchantPacketData):
        super().__init__(id=Packets.Enchant, opcode=opcode, data=data)
