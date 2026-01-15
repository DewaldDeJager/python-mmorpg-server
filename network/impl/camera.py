from ..packet import Packet
from ..packets import Packets
from ..opcodes import Camera as CameraOpcode

class CameraPacket(Packet):
    def __init__(self, opcode: CameraOpcode):
        super().__init__(id=Packets.Camera, opcode=opcode)
