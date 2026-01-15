from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..modules import ResourceState

class ResourcePacketData(CamelModel):
    instance: str
    state: ResourceState

class ResourcePacket(Packet):
    def __init__(self, data: ResourcePacketData):
        super().__init__(id=Packets.Resource, data=data)
