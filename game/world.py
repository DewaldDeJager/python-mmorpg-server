from __future__ import annotations

import asyncio
from typing import Optional, Callable, Awaitable

from common.config import config
from common.log import log
from database.mongodb import MongoDB
from game.packet_data import PacketData
from network.connection import Connection
from network.modules import PacketType
from network.network_manager import NetworkManager
from network.socket_handler import SocketHandler

ConnectionCallback = Callable[[Connection], Awaitable[None]]


class World:
    """
    The World class is an abstraction of where the players will be in.
    It keeps track of all players, entities, and events.
    """
    def __init__(self, socket_handler: SocketHandler, database: Optional[MongoDB] = None):
        self.socket_handler = socket_handler
        self.database = database
        self.network_manager = NetworkManager(self)

        self.max_players = config.max_players
        self.allow_connections = True

        self.connection_callback: Optional[ConnectionCallback] = None

        self.on_connection(self.network_manager.handle_connection)

        log.info('******************************************')

        self.tick()

    def tick(self) -> None:
        """
        Starts the server packet parsing and region updating loop. Every `config.update_time`
        we send all the packets in the queue to the players and update the regions.
        """
        async def update_loop():
            while True:
                await self.network_manager.parse()
                # TODO: self.map.regions.parse()
                await asyncio.sleep(config.update_time / 1000.0)

        async def save_loop():
            while True:
                await asyncio.sleep(config.save_interval / 1000.0)
                self.save()

        asyncio.create_task(update_loop())
        asyncio.create_task(save_loop())

    def push(self, packet_type: PacketType, data: PacketData) -> None:
        """
        All packets are sent through this function. Here we organize who we send the packet to,
        and perform further data checking (in the future if necessary).
        @param packet_type The method we are sending the packet.
        @param data The data containing information about who the packet is sent to.
        """
        if packet_type == PacketType.Broadcast:
            self.network_manager.broadcast(data.packet)
        elif packet_type == PacketType.Player:
            if data.player:
                self.network_manager.send(data.player.connection.instance, data.packet)
        elif packet_type == PacketType.Players:
            if data.players:
                instances = [player.connection.instance for player in data.players]
                self.network_manager.send_to_players(instances, data.packet)
        elif packet_type == PacketType.Region:
            if data.region:
                self.network_manager.send_to_region(data.region, data.packet, data.ignore)
        elif packet_type == PacketType.Regions:
            if data.region:
                self.network_manager.send_to_surrounding_regions(data.region, data.packet, data.ignore)

    def save(self) -> None:
        """
        Iterates through all the players currently logged in and saves their data.
        """
        # TODO: self.entities.for_each_player(lambda player: player.save())

        log.debug(f"{config.name} {config.server_id} has successfully saved.")

    def get_population(self) -> int:
        """
        Returns the number of players currently logged in.
        @returns Number of players logged in.
        """
        # TODO: Implement player tracking via Entities controller
        return 0

    def is_full(self) -> bool:
        """
        Checks if the world is full.
        @returns True if the number of players is equal to the max players.
        """
        return self.get_population() >= self.max_players

    def on_connection(self, callback: ConnectionCallback) -> None:
        """
        Sets the connection callback for the world.
        """
        self.connection_callback = callback
