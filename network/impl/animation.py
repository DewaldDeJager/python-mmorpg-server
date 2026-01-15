from typing import Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..modules import Actions

class AnimationPacketData(CamelModel):
    instance: str
    action: Actions
    resource_instance: Optional[str] = None

class AnimationPacket(Packet):
    def __init__(self, data: AnimationPacketData):
        super().__init__(id=Packets.Animation, data=data)
