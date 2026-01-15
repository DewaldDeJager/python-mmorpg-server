from ..packet import Packet
from ..packets import Packets
from .player import PlayerData

class SyncPacket(Packet):
    def __init__(self, data: PlayerData):
        super().__init__(id=Packets.Sync, data=data)
