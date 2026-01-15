from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets

class CommandPacketData(CamelModel):
    command: str

class CommandPacket(Packet):
    def __init__(self, data: CommandPacketData):
        super().__init__(id=Packets.Command, data=data)
