from typing import Dict, List, Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Ability as AbilityOpcode
from ..modules import AbilityType

class RawAbilityLevelData(CamelModel):
    cooldown: Optional[int] = None
    duration: Optional[int] = None
    mana: Optional[int] = None

class RawAbilityData(CamelModel):
    type: str
    levels: Optional[Dict[int, RawAbilityLevelData]] = None

class AbilityData(CamelModel):
    key: str
    level: int
    quick_slot: Optional[int] = None
    type: Optional[AbilityType] = None

class SerializedAbility(CamelModel):
    abilities: List[AbilityData]

AbilityPacketData = Union[SerializedAbility, AbilityData]

class AbilityPacket(Packet):
    def __init__(self, opcode: AbilityOpcode, data: AbilityPacketData):
        super().__init__(id=Packets.Ability, opcode=opcode, data=data)
