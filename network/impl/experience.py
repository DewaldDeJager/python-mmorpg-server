from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import Skills

class ExperiencePacketData(CamelModel):
    instance: str
    amount: Optional[int] = None
    level: Optional[int] = None
    skill: Optional[Skills] = None

class ExperiencePacket(Packet):
    def __init__(self, opcode: Opcodes.Experience, data: ExperiencePacketData):
        super().__init__(id=Packets.Experience, opcode=opcode, data=data)
