import pytest
import gzip
import json
import base64
from network.packets import Packets
from network.modules import (
    Orientation, Equipment as EquipmentModule, ContainerType, AbilityType, Actions,
    GuildRank, BannerColour, BannerOutline, BannerCrests, HealTypes, Interfaces,
    Effects, Skills, ResourceState, Ranks
)
from network.shared_types import (
    HitData, Hits, SerializedContainer, SlotData, EntityData, EntityDisplayInfo
)
from network.opcodes import (
    Movement as MovementOpcode, Combat as CombatOpcode, Equipment as EquipmentOpcode,
    Container as ContainerOpcode, Ability as AbilityOpcode, Achievement as AchievementOpcode,
    Bubble as BubbleOpcode, Camera as CameraOpcode, Crafting as CraftingOpcode,
    Effect as EffectOpcode, Enchant as EnchantOpcode, Experience as ExperienceOpcode,
    Friends as FriendsOpcode, Guild as GuildOpcode, Interface as InterfaceOpcode,
    List as ListOpcode, LootBag as LootBagOpcode, Minigame as MinigameOpcode,
    Network as NetworkOpcode, Notification as NotificationOpcode, NPC as NPCOpcode,
    Overlay as OverlayOpcode, Player as PlayerOpcode, Pointer as PointerOpcode,
    Quest as QuestOpcode, Skill as SkillOpcode, Store as StoreOpcode, Trade as TradeOpcode
)

# Imports for all packet implementations
from network.impl.handshake import HandshakePacket, ClientHandshakePacketData
from network.impl.movement import MovementPacket, MovementPacketData
from network.impl.combat import CombatPacket, CombatPacketData
from network.impl.equipment import EquipmentPacket, SerializedEquipment, EquipmentData
from network.impl.container import ContainerPacket, ContainerPacketData
from network.impl.chat import ChatPacket, ChatPacketData
from network.impl.ability import AbilityPacket, AbilityData, SerializedAbility
from network.impl.achievement import AchievementPacket, AchievementData, AchievementPacketData
from network.impl.animation import AnimationPacket, AnimationPacketData
from network.impl.blink import BlinkPacket
from network.impl.bubble import BubblePacket, BubblePacketData
from network.impl.camera import CameraPacket
from network.impl.command import CommandPacket, CommandPacketData
from network.impl.connected import ConnectedPacket
from network.impl.countdown import CountdownPacket, CountdownPacketData
from network.impl.crafting import CraftingPacket, CraftingPacketData, CraftingRequirement, CraftingResult
from network.impl.death import DeathPacket
from network.impl.despawn import DespawnPacket, DespawnPacketData
from network.impl.effect import EffectPacket, EffectPacketData
from network.impl.enchant import EnchantPacket, EnchantPacketData
from network.impl.experience import ExperiencePacket, ExperiencePacketData
from network.impl.friends import FriendsPacket, FriendsPacketData, FriendInfo
from network.impl.guild import GuildPacket, GuildPacketData, Member, Decoration, ListInfo
from network.impl.heal import HealPacket, HealPacketData
from network.impl.interface import InterfacePacket, InterfacePacketData
from network.impl.list import ListPacket, ListPacketData, Position
from network.impl.lootbag import LootBagPacket, LootBagPacketData
from network.impl.map import MapPacket
from network.impl.minigame import MinigamePacket, MinigamePacketData
from network.impl.music import MusicPacket
from network.impl.network import NetworkPacket, NetworkPacketData
from network.impl.notification import NotificationPacket, NotificationPacketData
from network.impl.npc import NPCPacket, NPCPacketData, NPCData
from network.impl.overlay import OverlayPacket, OverlayPacketData, SerializedLight
from network.impl.player import PlayerPacket, PlayerPacketData, PlayerData
from network.impl.pointer import PointerPacket, PointerPacketData
from network.impl.points import PointsPacket, PointsPacketData
from network.impl.poison import PoisonPacket
from network.impl.pvp import PVPPacket, PVPPacketData
from network.impl.quest import QuestPacket, QuestPacketData, QuestData
from network.impl.rank import RankPacket
from network.impl.relay import RelayPacket
from network.impl.resource import ResourcePacket, ResourcePacketData
from network.impl.respawn import RespawnPacket, RespawnPacketData
from network.impl.skill import SkillPacket, SkillPacketData, SkillData, SerializedSkills
from network.impl.spawn import SpawnPacket
from network.impl.store import StorePacket, StorePacketData, SerializedStoreItem
from network.impl.sync import SyncPacket
from network.impl.teleport import TeleportPacket, TeleportPacketData
from network.impl.trade import TradePacket, TradeRequestData, TradeAddData
from network.impl.update import UpdatePacket
from network.impl.welcome import WelcomePacket

def test_handshake_packet():
    data = ClientHandshakePacketData(type='client', instance='player_123', server_id=1)
    packet = HandshakePacket(data=data)
    expected = [Packets.Handshake.value, {'type': 'client', 'instance': 'player_123', 'serverId': 1}]
    assert packet.serialize() == expected

def test_movement_packet():
    data = MovementPacketData(instance='player_123', x=10, y=20, forced=False, orientation=Orientation.Up)
    packet = MovementPacket(opcode=MovementOpcode.Request, data=data)
    expected = [
        Packets.Movement.value,
        MovementOpcode.Request.value,
        {'instance': 'player_123', 'x': 10, 'y': 20, 'forced': False, 'orientation': 0}
    ]
    assert packet.serialize() == expected

def test_combat_packet():
    hit_data = HitData(type=Hits.Normal, damage=10, poison=True)
    data = CombatPacketData(instance='player_123', target='mob_456', hit=hit_data)
    packet = CombatPacket(opcode=CombatOpcode.Hit, data=data)
    expected = [
        Packets.Combat.value,
        CombatOpcode.Hit.value,
        {'instance': 'player_123', 'target': 'mob_456', 'hit': {'type': 0, 'damage': 10, 'poison': True}}
    ]
    assert packet.serialize() == expected

def test_equipment_packet_batch():
    eq_data = EquipmentData(type=EquipmentModule.Weapon, key='sword_1', count=1, enchantments={})
    data = SerializedEquipment(equipments=[eq_data])
    packet = EquipmentPacket(opcode=EquipmentOpcode.Batch, data=data)
    expected = [
        Packets.Equipment.value,
        EquipmentOpcode.Batch.value,
        {'equipments': [{'type': 4, 'key': 'sword_1', 'count': 1, 'enchantments': {}}]}
    ]
    assert packet.serialize() == expected

def test_container_packet():
    slot = SlotData(index=0, key='potion_1', count=5, enchantments={})
    container_data = SerializedContainer(slots=[slot])
    packet_data = ContainerPacketData(type=ContainerType.Inventory, data=container_data)
    packet = ContainerPacket(opcode=ContainerOpcode.Batch, data=packet_data)
    expected = [
        Packets.Container.value,
        ContainerOpcode.Batch.value,
        {'type': 1, 'data': {'slots': [{'index': 0, 'key': 'potion_1', 'count': 5, 'enchantments': {}}]}}
    ]
    assert packet.serialize() == expected

def test_chat_packet():
    data = ChatPacketData(message="Hello World", source="player_1", colour="white")
    packet = ChatPacket(data=data)
    expected = [Packets.Chat.value, {'message': "Hello World", 'source': "player_1", 'colour': "white"}]
    assert packet.serialize() == expected

def test_ability_packet():
    data = SerializedAbility(abilities=[AbilityData(key="fireball", level=1)])
    packet = AbilityPacket(opcode=AbilityOpcode.Batch, data=data)
    expected = [
        Packets.Ability.value,
        AbilityOpcode.Batch.value,
        {'abilities': [{'key': 'fireball', 'level': 1}]}
    ]
    assert packet.serialize() == expected

def test_achievement_packet():
    data = AchievementPacketData(achievements=[])
    packet = AchievementPacket(opcode=AchievementOpcode.Batch, data=data)
    expected = [Packets.Achievement.value, AchievementOpcode.Batch.value, {'achievements': []}]
    assert packet.serialize() == expected

def test_animation_packet():
    data = AnimationPacketData(instance="p1", action=Actions.Attack)
    packet = AnimationPacket(data=data)
    expected = [Packets.Animation.value, {'instance': 'p1', 'action': Actions.Attack.value}]
    assert packet.serialize() == expected

def test_blink_packet():
    packet = BlinkPacket(instance="item_1")
    expected = [Packets.Blink.value, "item_1"]
    assert packet.serialize() == expected

def test_bubble_packet():
    data = BubblePacketData(instance="p1", text="Hello")
    packet = BubblePacket(opcode=BubbleOpcode.Entity, data=data)
    expected = [Packets.Bubble.value, BubbleOpcode.Entity.value, {'instance': 'p1', 'text': 'Hello'}]
    assert packet.serialize() == expected

def test_camera_packet():
    packet = CameraPacket(opcode=CameraOpcode.LockX)
    expected = [Packets.Camera.value, CameraOpcode.LockX.value, None]
    assert packet.serialize() == expected

def test_command_packet():
    data = CommandPacketData(command="test")
    packet = CommandPacket(data=data)
    expected = [Packets.Command.value, {'command': 'test'}]
    assert packet.serialize() == expected

def test_connected_packet():
    packet = ConnectedPacket()
    expected = [Packets.Connected.value, None]
    assert packet.serialize() == expected

def test_countdown_packet():
    data = CountdownPacketData(instance="p1", time=10)
    packet = CountdownPacket(data=data)
    expected = [Packets.Countdown.value, {'instance': 'p1', 'time': 10}]
    assert packet.serialize() == expected

def test_crafting_packet():
    data = CraftingPacketData(type=Skills.Crafting)
    packet = CraftingPacket(opcode=CraftingOpcode.Open, data=data)
    expected = [Packets.Crafting.value, CraftingOpcode.Open.value, {'type': Skills.Crafting.value}]
    assert packet.serialize() == expected

def test_death_packet():
    packet = DeathPacket(instance="p1")
    expected = [Packets.Death.value, "p1"]
    assert packet.serialize() == expected

def test_despawn_packet():
    info = DespawnPacketData(instance="p1")
    packet = DespawnPacket(info=info)
    expected = [Packets.Despawn.value, {'instance': 'p1'}]
    assert packet.serialize() == expected

def test_effect_packet():
    data = EffectPacketData(instance="p1", effect=Effects.Stun)
    packet = EffectPacket(opcode=EffectOpcode.Add, data=data)
    expected = [Packets.Effect.value, EffectOpcode.Add.value, {'instance': 'p1', 'effect': Effects.Stun.value}]
    assert packet.serialize() == expected

def test_enchant_packet():
    data = EnchantPacketData(index=1)
    packet = EnchantPacket(opcode=EnchantOpcode.Select, data=data)
    expected = [Packets.Enchant.value, EnchantOpcode.Select.value, {'index': 1}]
    assert packet.serialize() == expected

def test_experience_packet():
    data = ExperiencePacketData(instance="p1", amount=100)
    packet = ExperiencePacket(opcode=ExperienceOpcode.Sync, data=data)
    expected = [Packets.Experience.value, ExperienceOpcode.Sync.value, {'instance': 'p1', 'amount': 100}]
    assert packet.serialize() == expected

def test_friends_packet():
    data = FriendsPacketData(list={})
    packet = FriendsPacket(opcode=FriendsOpcode.List, data=data)
    expected = [Packets.Friends.value, FriendsOpcode.List.value, {'list': {}}]
    assert packet.serialize() == expected

def test_guild_packet():
    # Test with complex nested data
    member = Member(username="user1", rank=GuildRank.Veteran, join_date=100, server_id=1)
    decoration = Decoration(
        banner=BannerColour.Red,
        outline=BannerOutline.StyleOne,
        outline_colour=BannerColour.Green,
        crest=BannerCrests.Star
    )

    data = GuildPacketData(
        name="MyGuild",
        members=[member],
        decoration=decoration,
        rank=GuildRank.Master
    )

    packet = GuildPacket(opcode=GuildOpcode.Create, data=data)

    expected = [
        Packets.Guild.value,
        GuildOpcode.Create.value,
        {
            'name': 'MyGuild',
            'members': [{'username': 'user1', 'rank': GuildRank.Veteran.value, 'joinDate': 100, 'serverId': 1}],
            'decoration': {
                'banner': BannerColour.Red.value,
                'outline': BannerOutline.StyleOne.value,
                'outlineColour': BannerColour.Green.value,
                'crest': BannerCrests.Star.value
            },
            'rank': GuildRank.Master.value
        }
    ]
    assert packet.serialize() == expected

def test_heal_packet():
    data = HealPacketData(instance="p1", type="hitpoints", amount=10)
    packet = HealPacket(data=data)
    expected = [Packets.Heal.value, {'instance': 'p1', 'type': 'hitpoints', 'amount': 10}]
    assert packet.serialize() == expected

def test_interface_packet():
    data = InterfacePacketData(identifier=Interfaces.Inventory)
    packet = InterfacePacket(opcode=InterfaceOpcode.Open, data=data)
    expected = [Packets.Interface.value, InterfaceOpcode.Open.value, {'identifier': Interfaces.Inventory.value}]
    assert packet.serialize() == expected

def test_list_packet():
    info = ListPacketData(entities=["e1", "e2"])
    packet = ListPacket(opcode=ListOpcode.Spawns, info=info)
    expected = [Packets.List.value, ListOpcode.Spawns.value, {'entities': ["e1", "e2"]}]
    assert packet.serialize() == expected

def test_lootbag_packet():
    info = LootBagPacketData(items=[])
    packet = LootBagPacket(opcode=LootBagOpcode.Open, info=info)
    expected = [Packets.LootBag.value, LootBagOpcode.Open.value, {'items': []}]
    assert packet.serialize() == expected

def test_map_packet():
    # Map packet is special, it compresses the data
    map_data = {'info': 'mapdata'}
    packet = MapPacket(data=map_data)
    serialized = packet.serialize()

    # Check ID
    assert serialized[0] == Packets.Map.value
    # Check data is base64 string
    assert isinstance(serialized[1], str)
    # Check buffer size exists
    assert isinstance(serialized[2], int)

    # Decode and verify
    decoded_bytes = base64.b64decode(serialized[1])
    decompressed = gzip.decompress(decoded_bytes)
    assert json.loads(decompressed) == map_data

def test_minigame_packet():
    data = MinigamePacketData(action=1)
    packet = MinigamePacket(opcode=MinigameOpcode.TeamWar, data=data)
    expected = [Packets.Minigame.value, MinigameOpcode.TeamWar.value, {'action': 1}]
    assert packet.serialize() == expected

def test_music_packet():
    packet = MusicPacket(new_song="song.mp3")
    expected = [Packets.Music.value, "song.mp3"]
    assert packet.serialize() == expected

def test_network_packet():
    data = NetworkPacketData(timestamp=123)
    packet = NetworkPacket(opcode=NetworkOpcode.Ping, data=data)
    expected = [Packets.Network.value, NetworkOpcode.Ping.value, {'timestamp': 123}]
    assert packet.serialize() == expected

def test_notification_packet():
    data = NotificationPacketData(message="Hi")
    packet = NotificationPacket(opcode=NotificationOpcode.Text, data=data)
    expected = [Packets.Notification.value, NotificationOpcode.Text.value, {'message': 'Hi'}]
    assert packet.serialize() == expected

def test_npc_packet():
    data = NPCPacketData(instance="npc1", text="Hello")
    packet = NPCPacket(opcode=NPCOpcode.Talk, data=data)
    expected = [Packets.NPC.value, NPCOpcode.Talk.value, {'instance': 'npc1', 'text': 'Hello'}]
    assert packet.serialize() == expected

def test_overlay_packet():
    data = OverlayPacketData(image="img.png")
    packet = OverlayPacket(opcode=OverlayOpcode.Set, data=data)
    expected = [Packets.Overlay.value, OverlayOpcode.Set.value, {'image': 'img.png'}]
    assert packet.serialize() == expected

def test_player_packet():
    data = PlayerPacketData(username="user")
    packet = PlayerPacket(opcode=PlayerOpcode.Login, data=data)
    expected = [Packets.Player.value, PlayerOpcode.Login.value, {'username': 'user'}]
    assert packet.serialize() == expected

def test_pointer_packet():
    data = PointerPacketData(x=1, y=2)
    packet = PointerPacket(opcode=PointerOpcode.Location, data=data)
    expected = [Packets.Pointer.value, PointerOpcode.Location.value, {'x': 1, 'y': 2}]
    assert packet.serialize() == expected

def test_points_packet():
    data = PointsPacketData(instance="p1", hit_points=10)
    packet = PointsPacket(data=data)
    # Note: hit_points becomes hitPoints via CamelModel
    expected = [Packets.Points.value, {'instance': 'p1', 'hitPoints': 10}]
    assert packet.serialize() == expected

def test_poison_packet():
    packet = PoisonPacket(type=1)
    expected = [Packets.Poison.value, 1]
    assert packet.serialize() == expected

def test_pvp_packet():
    data = PVPPacketData(state=True)
    packet = PVPPacket(data=data)
    expected = [Packets.PVP.value, {'state': True}]
    assert packet.serialize() == expected

def test_quest_packet():
    quest_data = QuestData(
        key="quest1",
        stage=1,
        sub_stage=0,
        completed_sub_stages=["sub1"]
    )
    data = QuestPacketData(quests=[quest_data])
    packet = QuestPacket(opcode=QuestOpcode.Batch, data=data)

    expected = [
        Packets.Quest.value,
        QuestOpcode.Batch.value,
        {
            'quests': [{
                'key': 'quest1',
                'stage': 1,
                'subStage': 0,
                'completedSubStages': ['sub1']
            }]
        }
    ]
    assert packet.serialize() == expected

def test_rank_packet():
    packet = RankPacket(rank=Ranks.Admin)
    expected = [Packets.Rank.value, Ranks.Admin.value]
    assert packet.serialize() == expected

def test_relay_packet():
    # Inner packet
    handshake_data = ClientHandshakePacketData(type='client', instance='p1', server_id=1)
    inner_packet = HandshakePacket(data=handshake_data)

    packet = RelayPacket(username="u1", packet=inner_packet)

    # Expected structure: [RelayID, [username, HandshakeID, {handshake data}]]
    # RelayPacket constructor sets data=[username, *serialized_packet]
    # serialize() does [id, data] (opcode is None)

    expected_inner = ['u1', Packets.Handshake.value, {'type': 'client', 'instance': 'p1', 'serverId': 1}]
    expected = [Packets.Relay.value, expected_inner]

    assert packet.serialize() == expected

def test_resource_packet():
    data = ResourcePacketData(instance="tree", state=ResourceState.Depleted)
    packet = ResourcePacket(data=data)
    expected = [Packets.Resource.value, {'instance': 'tree', 'state': ResourceState.Depleted.value}]
    assert packet.serialize() == expected

def test_respawn_packet():
    data = RespawnPacketData(x=1, y=2)
    packet = RespawnPacket(data=data)
    expected = [Packets.Respawn.value, {'x': 1, 'y': 2}]
    assert packet.serialize() == expected

def test_skill_packet():
    skill = SkillData(type=Skills.Alchemy, experience=1000, level=10)
    data = SerializedSkills(skills=[skill], cheater=False)
    packet = SkillPacket(opcode=SkillOpcode.Batch, data=data)

    expected = [
        Packets.Skill.value,
        SkillOpcode.Batch.value,
        {
            'skills': [{'type': Skills.Alchemy.value, 'experience': 1000, 'level': 10}],
            'cheater': False
        }
    ]
    assert packet.serialize() == expected

def test_spawn_packet():
    # Minimal EntityData
    data = EntityData(instance="e1", type=1, key="k", name="n", x=0, y=0)
    packet = SpawnPacket(data=data)
    # Note: CamelModel should handle conversion. All Optional=None are excluded.
    expected = [Packets.Spawn.value, {'instance': 'e1', 'type': 1, 'key': 'k', 'name': 'n', 'x': 0, 'y': 0}]
    assert packet.serialize() == expected

def test_store_packet():
    item = SerializedStoreItem(key="sword", name="Iron Sword", count=1, price=100)
    data = StorePacketData(key="general_store", items=[item], currency="gold")
    packet = StorePacket(opcode=StoreOpcode.Open, data=data)

    expected = [
        Packets.Store.value,
        StoreOpcode.Open.value,
        {
            'key': 'general_store',
            'currency': 'gold',
            'items': [{
                'key': 'sword',
                'name': 'Iron Sword',
                'count': 1,
                'price': 100
            }]
        }
    ]
    assert packet.serialize() == expected

def test_sync_packet():
    # Sync packet wraps PlayerData
    data = PlayerData(
        instance="p1", type=0, key="k", name="n", x=0, y=0,
        rank=Ranks.None_, pvp=False, equipments=[]
    )
    packet = SyncPacket(data=data)
    # Check some fields
    serialized = packet.serialize()
    assert serialized[0] == Packets.Sync.value
    payload = serialized[1]
    assert payload['instance'] == 'p1'
    assert payload['equipments'] == []
    # rank is enum, should be int value?
    # Ranks is IntEnum. json serialization might output int.
    # Pydantic's model_dump with enum should return int for IntEnum.
    assert payload['rank'] == Ranks.None_.value

def test_teleport_packet():
    data = TeleportPacketData(instance="p1", x=10, y=20)
    packet = TeleportPacket(data=data)
    expected = [Packets.Teleport.value, {'instance': 'p1', 'x': 10, 'y': 20}]
    assert packet.serialize() == expected

def test_trade_packet():
    data = TradeRequestData(instance="p2")
    packet = TradePacket(opcode=TradeOpcode.Request, data=data)
    expected = [Packets.Trade.value, TradeOpcode.Request.value, {'instance': 'p2'}]
    assert packet.serialize() == expected

def test_update_packet():
    data = [EntityDisplayInfo(instance="p1", scale=1.0)]
    packet = UpdatePacket(data=data)
    expected = [Packets.Update.value, [{'instance': 'p1', 'scale': 1.0}]]
    assert packet.serialize() == expected

def test_welcome_packet():
    # Welcome packet wraps PlayerData like Sync
    data = PlayerData(
        instance="p1", type=0, key="k", name="n", x=0, y=0,
        rank=Ranks.None_, pvp=False, equipments=[]
    )
    packet = WelcomePacket(data=data)
    serialized = packet.serialize()
    assert serialized[0] == Packets.Welcome.value
    assert serialized[1]['instance'] == 'p1'
