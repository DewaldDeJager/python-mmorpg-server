from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from pydantic import ConfigDict

if TYPE_CHECKING:
    from game.entity.character.player.player import Player

from network.packet import Packet
from network.model import CamelModel

class PacketData(CamelModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    packet: Packet
    player: Optional[Player] = None
    players: Optional[List[Player]] = None
    ignore: str = ""
    region: Optional[int] = None
    list: Optional[List[int]] = None
