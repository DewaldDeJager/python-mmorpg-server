from typing import List, Optional, TYPE_CHECKING
from network.socket_handler import SocketHandler
from database.database_manager import Database
from network.packet import Packet
from network.modules import PacketType
from network.model import CamelModel

if TYPE_CHECKING:
    from game.entity.character.player.player import Player

class PacketData(CamelModel):
    packet: Packet
    player: Optional["Player"] = None
    players: Optional[List["Player"]] = None
    ignore: str = ""
    region: Optional[int] = None
    list: Optional[List[int]] = None

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
