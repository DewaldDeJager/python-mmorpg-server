from ..packet import Packet
from ..packets import Packets

class BlinkPacket(Packet):
    def __init__(self, instance: str):
        super().__init__(id=Packets.Blink, data=instance)
