from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import Effects

class EffectPacketData(CamelModel):
    instance: str
    effect: Effects

class EffectPacket(Packet):
    def __init__(self, opcode: Opcodes.Effect, data: EffectPacketData):
        super().__init__(id=Packets.Effect, opcode=opcode, data=data)
