from typing import List, Dict, Optional, Literal
from pydantic import Field

from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Quest as QuestOpcode
from ..shared_types import PopupData
from .pointer import PointerData

class QuestItem(CamelModel):
    key: str
    count: int

class SkillReward(CamelModel):
    key: str
    experience: int

class RawStage(CamelModel):
    task: str
    npc: Optional[str] = None

    sub_stages: Optional[List['RawStage']] = None

    # Array of mob keys to kill.
    mob: Optional[List[str]] = None

    # How many of mobs to be killed.
    mob_count_requirement: Optional[int] = None

    # Item required in the inventory to progress to next stage.
    item_requirements: Optional[List[QuestItem]] = None

    # The items that we are rewarding the player for the stage.
    item_rewards: Optional[List[QuestItem]] = None

    # Text for the NPC.
    text: Optional[List[str]] = None
    completed_text: Optional[List[str]] = None
    has_item_text: Optional[List[str]] = None # Text for if the player has a required item/count in the inventory.

    # Pointer information
    pointer: Optional[PointerData] = None

    # Popup information
    popup: Optional[PopupData] = None

    # If the stage grants the user an ability.
    ability: Optional[str] = None
    ability_level: Optional[int] = None # Sets an ability to a level.

    # If a tree must be cut.
    tree: Optional[str] = None
    tree_count: Optional[int] = None # Amount of tress to be cut.

    # If a fish must be caught
    fish: Optional[str] = None
    fish_count: Optional[int] = None

    # If a rock must be mined
    rock: Optional[str] = None
    rock_count: Optional[int] = None

    # Skill experience rewards
    skill_rewards: Optional[List[SkillReward]] = None

    # Timer information for the stage
    timer: Optional[int] = None

HideNPC = Dict[str, str]

class RawQuest(CamelModel):
    name: str
    description: str
    rewards: Optional[List[str]] = None
    difficulty: Optional[str] = None
    skill_requirements: Optional[Dict[str, int]] = None # Skills required to start the quest.
    quest_requirements: Optional[List[str]] = None # Quests required to start this quest.
    hide_npcs: Optional[HideNPC] = Field(None, alias="hideNPCs") # NPCs to hide after quest.
    stages: Dict[int, RawStage]

class StageData(CamelModel):
    task: str
    npc: Optional[str] = None
    sub_stages: Optional[List[RawStage]] = None
    mob: Optional[List[str]] = None
    mob_count_requirement: int # how many mobs we need to kill to progress
    item_requirements: Optional[List[QuestItem]] = None
    item_rewards: Optional[List[QuestItem]] = None
    text: Optional[List[str]] = None
    completed_text: Optional[List[str]] = None
    pointer: Optional[PointerData] = None
    popup: Optional[PopupData] = None
    ability: Optional[str] = None
    ability_level: Optional[int] = None
    tree: Optional[str] = None
    tree_count: Optional[int] = None
    fish: Optional[str] = None
    fish_count: Optional[int] = None
    rock: Optional[str] = None
    rock_count: Optional[int] = None
    skill_rewards: Optional[List[SkillReward]] = None
    timer: Optional[int] = None

TaskType = Literal['talk', 'kill', 'pickup', 'tree']

class QuestData(CamelModel):
    key: str
    stage: int
    sub_stage: int
    completed_sub_stages: List[str]
    name: Optional[str] = None
    description: Optional[str] = None
    skill_requirements: Optional[Dict[str, int]] = None  # Skills required to start the quest.
    quest_requirements: Optional[List[str]] = None  # Quests required to start this quest.
    rewards: Optional[List[str]] = None
    difficulty: Optional[str] = None
    stage_count: Optional[int] = None

class SerializedQuest(CamelModel):
    quests: List[QuestData]

class QuestPacketData(CamelModel):
    key: Optional[str] = None
    stage: Optional[int] = None
    sub_stage: Optional[int] = None
    quests: Optional[List[QuestData]] = None  # Batch of quests
    interface_action: Optional[QuestOpcode] = Field(None, alias="interface")  # Interface actions

class QuestPacket(Packet):
    def __init__(self, opcode: QuestOpcode, data: QuestPacketData):
        super().__init__(id=Packets.Quest, opcode=opcode, data=data)

RawStage.model_rebuild()
