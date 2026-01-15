from typing import Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Container as ContainerOpcode
from ..modules import ContainerType
from ..shared_types import SerializedContainer, SlotData

class ContainerPacketData(CamelModel):
    type: ContainerType
    data: Optional[SerializedContainer] = None
    slot: Optional[SlotData] = None

class ContainerPacket(Packet):
    def __init__(self, opcode: ContainerOpcode, data: ContainerPacketData):
        super().__init__(id=Packets.Container, opcode=opcode, data=data)
