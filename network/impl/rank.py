from ..packet import Packet
from ..packets import Packets
from ..modules import Ranks

class RankPacket(Packet):
    def __init__(self, rank: Ranks):
        super().__init__(id=Packets.Rank, data=rank)
