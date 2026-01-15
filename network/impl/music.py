from typing import Optional
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets

MusicPacketData = Optional[str]

class MusicPacket(Packet):
    def __init__(self, new_song: Optional[str] = None):
        super().__init__(id=Packets.Music, data=new_song)
