from typing import List, Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets

class DespawnPacketData(CamelModel):
    instance: str # The entity we are despawning.
    regions: Optional[List[int]] = None # Region checker for when an entity despawns.

class DespawnPacket(Packet):
    def __init__(self, info: DespawnPacketData):
        super().__init__(id=Packets.Despawn, data=info)
