from typing import Optional, List
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes
from network.shared_types import EntityData
from network.modules import Ranks
from network.impl.equipment import EquipmentData

class PlayerPacketData(CamelModel):
    username: str
    server_id: Optional[int] = None
    guild: Optional[str] = None

class PlayerData(EntityData):
    rank: Ranks
    pvp: bool
    experience: Optional[int] = None
    next_experience: Optional[int] = None
    prev_experience: Optional[int] = None
    mana: Optional[int] = None
    max_mana: Optional[int] = None
    equipments: List[EquipmentData]

class PlayerPacket(Packet):
    def __init__(self, opcode: Opcodes.Player, data: Optional[PlayerPacketData] = None):
        super().__init__(id=Packets.Player, opcode=opcode, data=data)
