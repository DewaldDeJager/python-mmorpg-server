from typing import List, Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Skill as SkillOpcode
from ..modules import Skills

class SkillData(CamelModel):
    type: Skills
    experience: int
    level: Optional[int] = None
    percentage: Optional[int] = None
    next_experience: Optional[int] = None
    combat: Optional[bool] = None

class SerializedSkills(CamelModel):
    skills: List[SkillData]
    cheater: bool

SkillPacketData = Union[SerializedSkills, SkillData]

class SkillPacket(Packet):
    def __init__(self, opcode: SkillOpcode, data: Optional[SkillPacketData] = None):
        super().__init__(id=Packets.Skill, opcode=opcode, data=data)
