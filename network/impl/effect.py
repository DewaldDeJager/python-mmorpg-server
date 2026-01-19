from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.modules import Effects

class EffectPacketData(CamelModel):
    instance: str
    effect: Effects

class EffectPacket(Packet):
    def __init__(self, opcode: Opcodes.Effect, data: EffectPacketData):
        super().__init__(id=Packets.Effect, opcode=opcode, data=data)
