from typing import Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets

class TeleportPacketData(CamelModel):
    instance: str
    x: int
    y: int
    with_animation: Optional[bool] = None

class TeleportPacket(Packet):
    def __init__(self, data: TeleportPacketData):
        super().__init__(id=Packets.Teleport, data=data)
