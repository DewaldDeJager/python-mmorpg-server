from enum import IntEnum, auto
from typing import Dict, List, Union, Literal
from .opcodes import Pointer

# Assuming Pointer is imported from opcodes. If not, we might need to adjust imports.
# In TS it imports { Pointer } from './opcodes'.

EmptyPointer = {
    "type": Pointer.Remove
}

class PacketType(IntEnum):
    Broadcast = 0
    Player = 1
    Players = 2
    Region = 3
    Regions = 4
    RegionList = 5

class ContainerType(IntEnum):
    Bank = 0
    Inventory = 1
    Trade = 2
    LootBag = 3

class Orientation(IntEnum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

class EntityType(IntEnum):
    Player = 0
    NPC = 1
    Item = 2
    Mob = 3
    Chest = 4
    Projectile = 5
    Object = 6
    Pet = 7
    LootBag = 8
    Effect = 9
    Tree = 10
    Rock = 11
    Foraging = 12
    FishSpot = 13

class Interfaces(IntEnum):
    Inventory = 0
    Crafting = 1
    Spells = 2
    Bank = 3
    Store = 4
    Quests = 5
    Quest = 6
    Achievements = 7
    Skills = 8
    Trade = 9
    Settings = 10
    Warp = 11
    Leaderboards = 12
    Guilds = 13
    Friends = 14
    Enchant = 15
    Customization = 16
    Book = 17
    Lootbag = 18
    Equipments = 19
    Welcome = 20

class AbilityType(IntEnum):
    Active = 0
    Passive = 1

HealTypes = Literal['passive', 'hitpoints', 'mana']

class SpecialEntityTypes(IntEnum):
    Achievement = 0
    Quest = 1
    Area = 2
    Boss = 3
    Miniboss = 4

class Actions(IntEnum):
    Idle = 0
    Attack = 1
    Walk = 2
    Orientate = 3

# MenuActions uses string values.
from enum import Enum
class MenuActions(str, Enum):
    Attack = 'attack'
    Equip = 'equip'
    DropOne = 'drop-one'
    DropMany = 'drop-many'
    Eat = 'eat'
    Interact = 'interact'
    Trade = 'trade'
    Potion = 'potion'
    Follow = 'follow'
    Examine = 'examine'
    AddFriend = 'addfriend'

class InteractActions(IntEnum):
    pass # Empty enum

class Hits(IntEnum):
    Normal = 0
    Poison = 1
    Heal = 2
    Mana = 3
    Experience = 4
    LevelUp = 5
    Critical = 6
    Stun = 7
    Profession = 8
    Freezing = 9
    Burning = 10
    Terror = 11
    Explosive = 12

class Equipment(IntEnum):
    Helmet = 0
    Pendant = 1
    Arrows = 2
    Chestplate = 3
    Weapon = 4
    Shield = 5
    Ring = 6
    ArmourSkin = 7
    WeaponSkin = 8
    Legplates = 9
    Cape = 10
    Boots = 11

EquipmentRenderOrder = [
    Equipment.Cape,
    Equipment.Legplates,
    Equipment.Chestplate,
    Equipment.Helmet,
    Equipment.ArmourSkin,
    Equipment.Shield,
    Equipment.Weapon,
    Equipment.WeaponSkin
]

class AttackStyle(IntEnum):
    None_ = 0
    Stab = 1
    Slash = 2
    Defensive = 3
    Crush = 4
    Shared = 5
    Hack = 6
    Chop = 7
    Accurate = 8
    Fast = 9
    Focused = 10
    LongRange = 11

class Hovering(IntEnum):
    Colliding = 0
    Mob = 1
    Player = 2
    Item = 3
    NPC = 4
    Chest = 5
    Object = 6
    Tree = 7
    Rock = 8
    FishSpot = 9
    Foraging = 10

class AudioTypes(IntEnum):
    Music = 0
    SFX = 1

class PoisonTypes(IntEnum):
    Venom = 0
    Plague = 1
    Persistent = 2

class Warps(IntEnum):
    Mudwich = 0
    Aynor = 1
    Lakesworld = 2
    Patsow = 3
    Crullfield = 4
    Undersea = 5

class Skills(IntEnum):
    Lumberjacking = 0
    Accuracy = 1
    Archery = 2
    Health = 3
    Magic = 4
    Mining = 5
    Strength = 6
    Defense = 7
    Fishing = 8
    Cooking = 9
    Smithing = 10
    Crafting = 11
    Chiseling = 12
    Fletching = 13
    Smelting = 14
    Foraging = 15
    Eating = 16
    Loitering = 17
    Alchemy = 18

SkillsOrder = [
    Skills.Health,
    Skills.Accuracy,
    Skills.Strength,
    Skills.Defense,
    Skills.Archery,
    Skills.Magic,
    Skills.Lumberjacking,
    Skills.Mining,
    Skills.Fishing,
    Skills.Foraging,
    Skills.Crafting,
    Skills.Cooking,
    Skills.Fletching,
    Skills.Smithing,
    Skills.Alchemy,
    Skills.Eating,
    Skills.Loitering
]

class Enchantment(IntEnum):
    Bloodsucking = 0
    Critical = 1
    Evasion = 2
    Thorns = 3
    Explosive = 4
    Stun = 5
    AntiStun = 6
    Splash = 7
    DoubleEdged = 8

class Effects(IntEnum):
    None_ = 0
    Critical = 1
    Terror = 2
    TerrorStatus = 3
    Stun = 4
    Healing = 5
    Fireball = 6
    Iceball = 7
    Poisonball = 8
    Boulder = 9
    Running = 10
    HotSauce = 11
    DualistsMark = 12
    ThickSkin = 13
    SnowPotion = 14
    FirePotion = 15
    Burning = 16
    Freezing = 17
    Invincible = 18
    AccuracyBuff = 19
    StrengthBuff = 20
    DefenseBuff = 21
    MagicBuff = 22
    ArcheryBuff = 23
    AccuracySuperBuff = 24
    StrengthSuperBuff = 25
    DefenseSuperBuff = 26
    MagicSuperBuff = 27
    ArcherySuperBuff = 28
    Bleed = 29

class DamageStyle(IntEnum):
    None_ = 0
    Crush = 1
    Slash = 2
    Stab = 3
    Magic = 4
    Archery = 5

class Crowns(IntEnum):
    None_ = 0
    Silver = 1
    Gold = 2
    Artist = 3
    Tier1 = 4
    Tier2 = 5
    Tier3 = 6
    Tier4 = 7
    Tier5 = 8
    Tier6 = 9
    Tier7 = 10

class Ranks(IntEnum):
    None_ = 0
    Moderator = 1
    Admin = 2
    Veteran = 3
    Patron = 4
    Artist = 5
    Cheater = 6
    TierOne = 7
    TierTwo = 8
    TierThree = 9
    TierFour = 10
    TierFive = 11
    TierSix = 12
    TierSeven = 13
    HollowAdmin = 14
    Booster = 15

RankColours = {
    Ranks.None_: '',
    Ranks.Moderator: '#02f070',
    Ranks.Admin: '#3bbaff',
    Ranks.Veteran: '#d84343',
    Ranks.Patron: '#db753c',
    Ranks.Artist: '#b552f7',
    Ranks.Cheater: '#ffffff',
    Ranks.TierOne: '#db963c',
    Ranks.TierTwo: '#e6c843',
    Ranks.TierThree: '#d6e34b',
    Ranks.TierFour: '#a9e03a',
    Ranks.TierFive: '#7beb65',
    Ranks.TierSix: '#77e691',
    Ranks.TierSeven: '#77e691',
    Ranks.HollowAdmin: '#3bbaff',
    Ranks.Booster: '#f47fff'
}

RankTitles = {
    Ranks.None_: '',
    Ranks.Moderator: 'Mod',
    Ranks.Admin: 'Admin',
    Ranks.Veteran: 'Veteran',
    Ranks.Patron: 'Patron',
    Ranks.Artist: 'Artist',
    Ranks.Cheater: 'Cheater',
    Ranks.TierOne: 'T1 Patron',
    Ranks.TierTwo: 'T2 Patron',
    Ranks.TierThree: 'T3 Patron',
    Ranks.TierFour: 'T4 Patron',
    Ranks.TierFive: 'T5 Patron',
    Ranks.TierSix: 'T6 Patron',
    Ranks.TierSeven: 'T7 Patron',
    Ranks.HollowAdmin: 'Admin',
    Ranks.Booster: 'Booster'
}

# DamageColours omitted for brevity unless needed for server logic.
# It seems purely client-side rendering. But I'll include it if I want to be 1:1.
# The user asked for networking types.
# DamageColours is logic/data for rendering, not strictly type definition for packets, but it's in modules.ts.
# I will skip large dictionaries that are clearly client-side constants unless referenced in packets.
# RankColours is used? Maybe not in packets but shared config.
# I'll include Constants.

class NPCRole(IntEnum):
    Banker = 0
    Enchanter = 1
    Clerk = 2

class GuildRank(IntEnum):
    Fledgling = 0
    Emergent = 1
    Established = 2
    Adept = 3
    Veteran = 4
    Elite = 5
    Master = 6
    Landlord = 7

class BannerColour(str, Enum):
    Grey = 'grey'
    Green = 'green'
    Fuchsia = 'fuchsia'
    Red = 'red'
    Brown = 'brown'
    Cyan = 'cyan'
    DarkGrey = 'darkgrey'
    Teal = 'teal'
    GoldenYellow = 'goldenyellow'

class BannerOutline(IntEnum):
    StyleOne = 0
    StyleTwo = 1
    StyleThree = 2
    StyleFour = 3
    StyleFive = 4

class BannerCrests(str, Enum):
    None_ = 'none'
    Star = 'star'
    Hawk = 'hawk'
    Phoenix = 'phoenix'

class Constants:
    MAX_STACK = 2_147_483_647
    MAX_LEVEL = 120
    INVENTORY_SIZE = 25
    BANK_SIZE = 420
    DROP_PROBABILITY = 100_000
    MAX_PROFESSION_LEVEL = 99
    HEAL_RATE = 7000
    EFFECT_RATE = 10_000
    STORE_UPDATE_FREQUENCY = 20_000
    MAP_DIVISION_SIZE = 48
    SPAWN_POINT = '328,892'
    TUTORIAL_QUEST_KEY = 'tutorial'
    ALCHEMY_QUEST_KEY = 'scientistspotion'
    CRAFTING_QUEST_KEY = 'artsandcrafts'
    TUTORIAL_SPAWN_POINT = '133,562'
    JAIL_SPAWN_POINT = '110,915'
    RESOURCE_RESPAWN = 30_000
    TREE_RESPAWN = 25_000
    CHEST_RESPAWN = 50_000
    SKILL_LOOP = 1000
    MAX_ACCURACY = 0.45
    EDIBLE_COOLDOWN = 1500
    CRAFT_COOLDOWN = 1500
    ARCHER_ATTACK_RANGE = 8
    MAX_CONNECTIONS = 16
    EXPERIENCE_PER_HIT = 2
    SNOW_POTION_DURATION = 60_000
    FIRE_POTION_DURATION = 60_000
    FREEZING_DURATION = 60_000
    BURNING_DURATION = 60_000
    TERROR_DURATION = 60_000
    LOITERING_THRESHOLD = 90_000
    STUN_DURATION = 10_000
    COLD_EFFECT_DAMAGE = 10
    BURNING_EFFECT_DAMAGE = 20
    ATTACKER_TIMEOUT = 20_000
    MAX_GUILD_MEMBERS = 50
    EVENTS_CHECK_INTERVAL = 3_600_000

class MinigameConstants:
    TEAM_WAR_COUNTDOWN = 240
    TEAM_WAR_MIN_PLAYERS = 2
    COURSING_COUNTDOWN = 45
    COURSING_MIN_PLAYERS = 2
    COURSING_SCORE_DIVISOR = 10

class APIConstants(IntEnum):
    UNHANDLED_HTTP_METHOD = 0
    NOT_FOUND_ERROR = 1
    MALFORMED_PARAMETERS = 2
    PLAYER_NOT_ONLINE = 3

class Defaults:
    MOVEMENT_SPEED = 220
    ATTACK_RATE = 1000
    POISON_CHANCE = 15

class ItemDefaults:
    RESPAWN_DELAY = 30_000
    DESPAWN_DURATION = 34_000
    BLINK_DELAY = 30_000

class MobDefaults:
    AGGRO_RANGE = 2
    RESPAWN_DELAY = 60_000
    ROAM_DISTANCE = 7
    ROAM_FREQUENCY = 17_000
    HEALTH_LEVEL = 1
    ACCURACY_LEVEL = 1
    STRENGTH_LEVEL = 1
    DEFENSE_LEVEL = 1
    MAGIC_LEVEL = 1
    ARCHERY_LEVEL = 1
    ATTACK_LEVEL = 1

class MapFlags(IntEnum):
    DIAGONAL_FLAG = 0x20_00_00_00
    VERTICAL_FLAG = 0x40_00_00_00
    HORIZONTAL_FLAG = 0x80_00_00_00

class ResourceState(IntEnum):
    Default = 0
    Depleted = 1
