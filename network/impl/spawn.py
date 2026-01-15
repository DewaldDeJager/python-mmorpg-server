from ..packet import Packet
from ..packets import Packets
from ..shared_types import EntityData

class SpawnPacket(Packet):
    def __init__(self, data: EntityData):
        super().__init__(id=Packets.Spawn, data=data)
