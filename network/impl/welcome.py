from ..packet import Packet
from ..packets import Packets
from .player import PlayerData

class WelcomePacket(Packet):
    def __init__(self, data: PlayerData):
        super().__init__(id=Packets.Welcome, data=data)
