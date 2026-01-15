from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets

class DeathPacket(Packet):
    def __init__(self, instance: str):
        super().__init__(id=Packets.Death, data=instance)
