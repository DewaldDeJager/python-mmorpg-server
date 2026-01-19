from typing import Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.modules import Skills

class ExperiencePacketData(CamelModel):
    instance: str
    amount: Optional[int] = None
    level: Optional[int] = None
    skill: Optional[Skills] = None

class ExperiencePacket(Packet):
    def __init__(self, opcode: Opcodes.Experience, data: ExperiencePacketData):
        super().__init__(id=Packets.Experience, opcode=opcode, data=data)
