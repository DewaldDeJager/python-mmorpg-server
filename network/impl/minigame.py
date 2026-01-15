from typing import Optional
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class MinigamePacketData(CamelModel):
    action: int
    countdown: Optional[int] = None
    score: Optional[int] = None
    red_team_kills: Optional[int] = None
    blue_team_kills: Optional[int] = None
    started: Optional[bool] = None

class MinigamePacket(Packet):
    def __init__(self, opcode: Opcodes.Minigame, data: Optional[MinigamePacketData] = None):
        super().__init__(id=Packets.Minigame, opcode=opcode, data=data)
