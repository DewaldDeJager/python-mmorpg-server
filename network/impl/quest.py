from typing import List, Dict, Optional
from pydantic import Field

from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Quest as QuestOpcode

class QuestData(CamelModel):
    key: str
    stage: int
    sub_stage: int
    completed_sub_stages: List[str]
    name: Optional[str] = None
    description: Optional[str] = None
    skill_requirements: Optional[Dict[str, int]] = None
    quest_requirements: Optional[List[str]] = None
    rewards: Optional[List[str]] = None
    difficulty: Optional[str] = None
    stage_count: Optional[int] = None

class SerializedQuest(CamelModel):
    quests: List[QuestData]

class QuestPacketData(CamelModel):
    key: Optional[str] = None
    stage: Optional[int] = None
    sub_stage: Optional[int] = None
    quests: Optional[List[QuestData]] = None
    interface_action: Optional[QuestOpcode] = Field(None, alias="interface")

class QuestPacket(Packet):
    def __init__(self, opcode: QuestOpcode, data: QuestPacketData):
        super().__init__(id=Packets.Quest, opcode=opcode, data=data)
