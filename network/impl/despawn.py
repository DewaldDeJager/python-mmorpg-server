from typing import List, Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets

class DespawnPacketData(CamelModel):
    instance: str
    regions: Optional[List[int]] = None

class DespawnPacket(Packet):
    def __init__(self, info: DespawnPacketData):
        super().__init__(id=Packets.Despawn, data=info)
