from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets

class CountdownPacketData(CamelModel):
    instance: str
    time: int

class CountdownPacket(Packet):
    def __init__(self, data: CountdownPacketData):
        super().__init__(id=Packets.Countdown, data=data)
