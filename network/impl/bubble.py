from typing import Any, Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Bubble

class BubblePacketData(CamelModel):
    instance: str
    text: str
    duration: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

class BubblePacket(Packet):
    def __init__(self, data: Any, opcode: Bubble = Bubble.Entity):
        super().__init__(id=Packets.Bubble, opcode=opcode, data=data)
