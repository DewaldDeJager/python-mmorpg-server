from typing import Dict, List, Optional
from pydantic import BaseModel
from .model import CamelModel
from .modules import Hits, Orientation
class Enchantment(CamelModel):
    level: int

# Enchantments is a dict of id (number) -> Enchantment
Enchantments = Dict[int, Enchantment]

class Stats(CamelModel):
    crush: int
    slash: int
    stab: int
    archery: int
    magic: int

class Bonuses(CamelModel):
    accuracy: int
    strength: int
    archery: int
    magic: int

# This is for items that have a lamp effect.
class LampData(CamelModel):
    distance: int
    colour: str
    flicker_speed: int
    flicker_intensity: int

class Light(CamelModel):
    outer: Optional[LampData] = None
    inner: Optional[LampData] = None

class SlotData(CamelModel):
    index: int
    key: str
    count: int
    enchantments: Enchantments
    name: Optional[str] = None
    description: Optional[str] = None
    edible: Optional[bool] = None
    interactable: Optional[bool] = None
    equippable: Optional[bool] = None
    price: Optional[int] = None
    attack_stats: Optional[Stats] = None
    defense_stats: Optional[Stats] = None
    bonuses: Optional[Bonuses] = None

class SerializedContainer(CamelModel):
    username: Optional[str] = None
    slots: List[SlotData]

class HitData(CamelModel):
    type: Hits
    damage: int
    ranged: Optional[bool] = None
    aoe: Optional[int] = None
    terror: Optional[bool] = None
    poison: Optional[bool] = None
    skills: Optional[List[str]] = None

class HubChatPacketData(CamelModel):
    source: str
    message: Optional[str] = None
    colour: Optional[str] = None
    target: Optional[str] = None
    success: Optional[bool] = None
    not_found: Optional[bool] = None

class PopupData(CamelModel):
    title: str
    text: str
    colour: Optional[str] = None
    sound_effect: Optional[str] = None

class EntityDisplayInfo(CamelModel):
    instance: str
    colour: Optional[str] = None
    scale: Optional[float] = None
    exclamation: Optional[str] = None

class EntityData(CamelModel):
    # Entity data
    instance: str
    type: int
    key: str
    name: str
    x: int
    y: int

    # Optional parameters
    colour: Optional[str] = None  # Name colour
    scale: Optional[float] = None  # Custom scale for the entity

    # Character data
    movement_speed: Optional[int] = None
    hit_points: Optional[int] = None
    max_hit_points: Optional[int] = None
    attack_range: Optional[int] = None
    level: Optional[int] = None
    hidden_name: Optional[bool] = None
    orientation: Optional[Orientation] = None

    # Item data
    count: Optional[int] = None
    enchantments: Optional[Enchantments] = None

    # Projectile data
    owner_instance: Optional[str] = None
    target_instance: Optional[str] = None
    hit: Optional[HitData] = None

    display_info: Optional[EntityDisplayInfo] = None
