from ..packet import Packet
from ..packets import Packets

class ConnectedPacket(Packet):
    def __init__(self):
        super().__init__(id=Packets.Connected)
