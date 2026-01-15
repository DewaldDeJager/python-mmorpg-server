from typing import List, Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Achievement as AchievementOpcode

class RawAchievement(CamelModel):
    name: str
    description: Optional[str] = None
    region: Optional[str] = None
    hidden: Optional[bool] = None
    secret: Optional[bool] = None
    npc: Optional[str] = None
    dialogue_hidden: Optional[List[str]] = None
    dialogue_started: Optional[List[str]] = None
    mob: Optional[Union[str, List[str]]] = None
    mob_count: Optional[int] = None
    item: Optional[str] = None
    item_count: Optional[int] = None
    reward_item: Optional[str] = None
    reward_item_count: Optional[int] = None
    reward_skill: Optional[str] = None
    reward_experience: Optional[int] = None
    reward_ability: Optional[str] = None
    reward_ability_level: Optional[int] = None

class AchievementData(CamelModel):
    key: str
    name: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None
    stage: int
    stage_count: Optional[int] = None
    secret: Optional[bool] = None

class SerializedAchievement(CamelModel):
    achievements: List[AchievementData]

class AchievementPacketData(CamelModel):
    key: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[int] = None
    achievements: Optional[List[AchievementData]] = None

class AchievementPacket(Packet):
    def __init__(self, opcode: AchievementOpcode, data: AchievementPacketData):
        super().__init__(id=Packets.Achievement, opcode=opcode, data=data)
