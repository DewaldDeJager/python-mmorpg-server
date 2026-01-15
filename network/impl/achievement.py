from typing import List, Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Achievement as AchievementOpcode

class RawAchievement(CamelModel):
    name: str
    description: Optional[str] = None
    region: Optional[str] = None  # The region that the achievement belongs to.
    hidden: Optional[bool] = None  # Whether or not to display description and achievement title.
    secret: Optional[bool] = None  # Secret achievements are only displayed when completed.
    npc: Optional[str] = None  # NPC handing out the achievement.
    dialogue_hidden: Optional[List[str]] = None  # Dialogue to display before the achievement is discovered.
    dialogue_started: Optional[List[str]] = None  # Dialogue when the achievement has been started.
    mob: Optional[Union[str, List[str]]] = None  # If the achievement requires a mob (or mobs) to be killed.
    mob_count: Optional[int] = None  # How many of the mobs to be killed.
    item: Optional[str] = None  # If the achievement requires an item to be found.
    item_count: Optional[int] = None  # How much of an item to bring.
    reward_item: Optional[str] = None  # String of the item we are rewarding.
    reward_item_count: Optional[int] = None  # How much of the item to reward.
    reward_skill: Optional[str] = None  # Skill we are rewarding experience in.
    reward_experience: Optional[int] = None  # How much experience to reward.
    reward_ability: Optional[str] = None  # Key of the ability that is being rewarded.
    reward_ability_level: Optional[int] = None  # Optional, otherwise defaults to 1.

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
