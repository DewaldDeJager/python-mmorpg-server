from typing import List, Optional, Union
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes
from packages.server_python.network.modules import Equipment as EquipmentModule, AttackStyle
from packages.server_python.network.shared_types import Enchantments, Stats, Bonuses, Light

class EquipmentData(CamelModel):
    type: EquipmentModule
    key: str
    name: Optional[str] = None
    count: int
    enchantments: Enchantments
    attack_range: Optional[int] = None
    poisonous: Optional[bool] = None
    attack_stats: Optional[Stats] = None
    defense_stats: Optional[Stats] = None
    bonuses: Optional[Bonuses] = None
    attack_style: Optional[AttackStyle] = None
    attack_styles: Optional[List[AttackStyle]] = None
    bow: Optional[bool] = None
    archer: Optional[bool] = None
    light: Optional[Light] = None

class SerializedEquipment(CamelModel):
    equipments: List[EquipmentData]

class UnequipData(CamelModel):
    type: EquipmentModule
    count: Optional[int] = None

class StyleData(CamelModel):
    attack_style: AttackStyle
    attack_range: int

# Union of all possible data types
EquipmentPacketData = Union[SerializedEquipment, EquipmentData, UnequipData, StyleData]

class EquipmentPacket(Packet):
    def __init__(self, opcode: Opcodes.Equipment, data: EquipmentPacketData):
        super().__init__(id=Packets.Equipment, opcode=opcode, data=data)
