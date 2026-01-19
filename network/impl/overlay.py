from typing import Optional
from network.model import CamelModel
from network.packet import Packet
from network.packets import Packets
from network import opcodes as Opcodes

class SerializedLight(CamelModel):
    instance: str
    x: int
    y: int
    colour: str
    diffuse: int
    distance: int
    flicker_speed: int
    flicker_intensity: int
    entity: Optional[str] = None

class OverlayPacketData(CamelModel):
    image: Optional[str] = None
    colour: Optional[str] = None
    light: Optional[SerializedLight] = None

class OverlayPacket(Packet):
    def __init__(self, opcode: Opcodes.Overlay, data: Optional[OverlayPacketData] = None):
        super().__init__(id=Packets.Overlay, opcode=opcode, data=data)
