from typing import List, Optional, Dict
from packages.server_python.network.model import CamelModel
from packages.server_python.network.modules import Ranks, Orientation
from packages.server_python.network.impl.equipment import SerializedEquipment
from packages.server_python.network.shared_types import SerializedContainer
from packages.server_python.network.impl.quest import SerializedQuest
from packages.server_python.network.impl.achievement import SerializedAchievement
from packages.server_python.network.impl.skill import SerializedSkills
from packages.server_python.network.impl.ability import SerializedAbility

class ResetToken(CamelModel):
    token: str
    expiration: int

class PoisonInfo(CamelModel):
    type: int # Type of poison.
    remaining: int # How much of the poison is left.

class SerializedDuration(CamelModel):
    remaining_time: int

# Maps effect ID to duration
SerializedEffects = Dict[int, SerializedDuration]

class PlayerInfo(CamelModel):
    username: str
    password: str
    email: str
    x: int
    y: int
    user_agent: str
    rank: Ranks
    poison: PoisonInfo
    effects: SerializedEffects
    hit_points: int
    mana: int
    orientation: Orientation
    ban: int
    jail: int
    mute: int
    last_warp: int
    map_version: int
    regions_loaded: List[int]
    friends: List[str]
    last_server_id: int
    last_address: str
    last_global_chat: int
    guild: str
    pet: str
    reset_token: Optional[ResetToken] = None

# Wrappers for other collections that store serialized packet data keyed by username
class PlayerEquipmentModel(SerializedEquipment):
    username: str

class PlayerInventoryModel(SerializedContainer):
    username: str

class PlayerBankModel(SerializedContainer):
    username: str

class PlayerQuestsModel(SerializedQuest):
    username: str

class PlayerAchievementsModel(SerializedAchievement):
    username: str

class PlayerSkillsModel(SerializedSkills):
    username: str

class PlayerAbilitiesModel(SerializedAbility):
    username: str
