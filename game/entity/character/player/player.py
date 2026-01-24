import asyncio
from datetime import datetime
from typing import Dict, List

from common.log import log
from game.entity.character.character import Character
from game.info.formulas import Formulas
from game.world import World
from network.connection import Connection
from network.impl.connected import ConnectedPacket
from network.impl.welcome import WelcomePacket
from network.impl.points import PointsPacket, PointsPacketData
from network.impl.player import PlayerData, PlayerPacket, PlayerPacketData
from game.packet_data import PacketData
from network.modules import PacketType, Ranks, AttackStyle, PoisonTypes
from network.packet import Packet
from network import opcodes as Opcodes
from game.entity.character.player.incoming import Incoming
from database.models.player import PlayerInfo
from game.entity.character.points.mana import Mana


class Player(Character):

    def __init__(self, world: World, connection: Connection):
        super().__init__(connection.instance, world, "", -1, -1)

        self.world = world
        self.connection = connection

        self.incoming = Incoming(self)

        self.mana = Mana(Formulas.get_max_mana(self.level))
        self.mana.on_mana(self.handle_mana)

        self.ready = False  # indicates if login processed finished
        self.authenticated = False
        self.is_guest = False

        # Player info
        self.username = ""
        self.password = ""
        self.email = ""
        self.user_agent = ""
        self.guild = ""

        self.rank = Ranks.None_

        # Stores the last attack style for each type of weapon.
        self.last_styles: Dict[str, AttackStyle] = {}

        # Warps
        self.last_warp = 0

        # Moderation variables
        self.ban = 0  # epoch timestamp
        self.mute = 0
        self.jail = 0

        # Player miscellaneous data
        self.map_version = -1

        # Region data
        self.regions_loaded: List[int] = []

        self.connection.on_close(self.handle_close)


    async def load(self, data: PlayerInfo) -> None:
        """
        Loads the player data from the database. This is a crucial
        method as it ensures that the player's information is
        fully loaded from the database prior to calculating region data.
        @param data PlayerInfo object containing all data.
        """
        # The player's ban timestamp is in the future, so they are still banned.
        if data.ban > datetime.now().timestamp() * 1000:
            return await self.connection.reject("banned")

        # Store coords for when we're done loading.
        self.x = data.x
        self.y = data.y
        self.name = data.username
        self.username = data.username
        self.guild = data.guild
        self.rank = data.rank or Ranks.None_
        self.ban = data.ban
        self.jail = data.jail
        self.mute = data.mute
        self.orientation = data.orientation
        self.map_version = data.map_version
        self.user_agent = data.user_agent
        self.regions_loaded = data.regions_loaded or []
        # self.last_global_chat = data.last_global_chat or 0

        if data.poison:
            self.set_poison(PoisonTypes(data.poison.type) if data.poison.type else None,
                            datetime.fromtimestamp((datetime.now().timestamp() * 1000 - data.poison.remaining) / 1000))
        self.set_last_warp(data.last_warp)

        self.hit_points.update_hit_points(data.hit_points)
        self.mana.update_mana(data.mana)

        # self.friends.load(data.friends)

        # self.load_skills()
        # self.load_equipment()
        # self.load_inventory()
        # self.load_bank()
        # self.load_statistics()
        # self.load_abilities()

        # Synchronize login with the hub's server list.
        self.world.push(PacketType.Player, PacketData(
            packet=PlayerPacket(Opcodes.Player.Login, PlayerPacketData(username=self.username, guild=self.guild)),
            player=self
        ))

        # Quests and achievements have to be loaded prior to introducing the player.
        # await self.load_quests()
        # await self.load_achievements()

        self.intro()

        # Connect the player to their guild if they are in one.
        # if self.guild:
        #     self.world.guilds.connect(self, self.guild)

        # Spawn the pet if the player has one.
        # if data.pet:
        #     self.set_pet(data.pet)

        # Apply the status effects from the database.
        # self.status.load(data.effects)

    def intro(self) -> None:
        """
        Handle the actual player login. Check if the user is banned,
        update hitPoints and mana, and send the player information
        to the client.
        """
        # Reset hitpoints if they are uninitialized.
        if self.hit_points.get_hit_points() < 0:
            self.hit_points.set_hit_points(self.hit_points.get_max_hit_points())

        # Reset mana if it is uninitialized.
        if self.mana.get_mana() < 0:
            self.mana.set_mana(self.mana.get_max_mana())

        # Update the player's timeout based on their rank.
        if self.rank != Ranks.None_:
            # self.connection.update_timeout(self.get_timeout_by_rank())
            pass

        # Timeout the player if the ready packet is not received within 10 seconds.
        async def ready_timeout_task():
            await asyncio.sleep(7)
            if not self.ready or self.connection.closed:
                await self.connection.reject("error")

        asyncio.create_task(ready_timeout_task())

        self.set_position(self.x, self.y)

        # self.entities.add_player(self)

        self.send(WelcomePacket(self.serialize(False, True, True)))

    def set_last_warp(self, last_warp: int) -> None:
        self.last_warp = last_warp

    def handle_mana(self) -> None:
        self.send(PointsPacket(PointsPacketData(
            instance=self.instance,
            mana=self.mana.get_mana(),
            max_mana=self.mana.get_max_mana()
        )))

    def handle_close(self) -> None:
        log.info(f"Closing player: {self.connection.address}")
        self.stop_intervals()

    def send(self, packet: Packet) -> None:
        """
        We create this function to make it easier to send
        packets to players instead of always importing `world`
        in other classes.
        @param packet Packet we are sending to the player.
        """
        self.world.push(PacketType.Player, PacketData(packet=packet, player=self))

    def serialize(self, with_equipment: bool = False, with_experience: bool = False,
                  with_mana: bool = False) -> PlayerData:
        entity_data = super().serialize()

        # Create PlayerData from EntityData
        data = PlayerData(
            instance=entity_data.instance,
            type=entity_data.type,
            key=entity_data.key,
            name=entity_data.name,
            x=entity_data.x,
            y=entity_data.y,
            rank=self.rank,
            pvp=False,  # TODO: Implement PVP status
            equipments=[]  # TODO: Implement equipment serialization
        )

        # Copy optional fields from entity_data if they exist
        data.colour = entity_data.colour
        data.scale = entity_data.scale
        data.movement_speed = entity_data.movement_speed
        data.hit_points = entity_data.hit_points
        data.max_hit_points = entity_data.max_hit_points
        data.attack_range = entity_data.attack_range
        data.level = entity_data.level
        data.hidden_name = entity_data.hidden_name
        data.orientation = entity_data.orientation

        if with_mana:
            data.mana = self.mana.get_mana()
            data.max_mana = self.mana.get_max_mana()

        if with_experience:
            # TODO: Implement experience serialization
            data.experience = 0
            data.next_experience = 0
            data.prev_experience = 0

        return data


PacketData.model_rebuild()
