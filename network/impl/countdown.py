from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets

class CountdownPacketData(CamelModel):
    instance: str
    time: int

class CountdownPacket(Packet):
    def __init__(self, data: CountdownPacketData):
        super().__init__(id=Packets.Countdown, data=data)
