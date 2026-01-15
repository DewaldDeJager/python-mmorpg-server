from typing import Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Movement as MovementOpcode
from ..modules import Orientation

class MovementPacketData(CamelModel):
    instance: str
    x: Optional[int] = None
    y: Optional[int] = None
    forced: Optional[bool] = None
    target: Optional[str] = None
    orientation: Optional[Orientation] = None
    state: Optional[bool] = None
    movement_speed: Optional[int] = None

class MovementPacket(Packet):
    def __init__(self, opcode: MovementOpcode, data: Optional[MovementPacketData] = None):
        super().__init__(id=Packets.Movement, opcode=opcode, data=data)
