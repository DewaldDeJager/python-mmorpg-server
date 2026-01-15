from typing import List
from ..packet import Packet
from ..packets import Packets
from ..shared_types import EntityDisplayInfo

class UpdatePacket(Packet):
    def __init__(self, data: List[EntityDisplayInfo]):
        super().__init__(id=Packets.Update, data=data)
