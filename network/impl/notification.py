from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class NotificationPacketData(CamelModel):
    title: Optional[str] = None
    message: str
    colour: Optional[str] = None
    source: Optional[str] = None
    sound_effect: Optional[str] = None

class NotificationPacket(Packet):
    def __init__(self, opcode: Opcodes.Notification, data: NotificationPacketData):
        super().__init__(id=Packets.Notification, opcode=opcode, data=data)
