from typing import Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Movement as MovementOpcode
from ..modules import Orientation

class MovementPacketData(CamelModel):
    instance: str # Main entity involved in the movement.
    x: Optional[int] = None # X coordinate of the movement.
    y: Optional[int] = None # Y coordinate of the movement.
    forced: Optional[bool] = None # Whether or not the movement is forced.
    target: Optional[str] = None # Entity instance we are trying to follow if specified.
    orientation: Optional[Orientation] = None
    state: Optional[bool] = None # State about stun/freeze.
    movement_speed: Optional[int] = None # Movement speed of the entity.

class MovementPacket(Packet):
    def __init__(self, opcode: MovementOpcode, data: Optional[MovementPacketData] = None):
        super().__init__(id=Packets.Movement, opcode=opcode, data=data)
