from __future__ import annotations
from network.socket_handler import SocketHandler
from database.database_manager import Database
from network.packet import Packet
from network.modules import PacketType
from game.packet_data import PacketData

class World:
    """
    A stub World class to satisfy the Character dependency.
    """
    def __init__(self, socket_handler: SocketHandler, database: Database):
        self.socket_handler = socket_handler
        self.database = database

    def push(self, packet_type: PacketType, data: PacketData) -> None:
        """
        Push a packet to the network queue.
        """
        pass
