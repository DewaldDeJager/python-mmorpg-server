from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Combat as CombatOpcode
from ..shared_types import HitData

class CombatPacketData(CamelModel):
    instance: str
    target: str
    hit: HitData

class CombatPacket(Packet):
    def __init__(self, opcode: CombatOpcode, data: CombatPacketData):
        super().__init__(id=Packets.Combat, opcode=opcode, data=data)
