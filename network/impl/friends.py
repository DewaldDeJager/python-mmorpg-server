from typing import Optional, Dict
from packages.server_python.network.model import CamelModel
from packages.server_python.network.packet import Packet
from packages.server_python.network.packets import Packets
from packages.server_python.network import opcodes as Opcodes

class FriendInfo(CamelModel):
    online: bool
    server_id: int

# Type alias for Friend dict
Friend = Dict[str, FriendInfo]

class FriendsPacketData(CamelModel):
    list: Optional[Friend] = None
    username: Optional[str] = None
    status: Optional[bool] = None
    server_id: Optional[int] = None

class FriendsPacket(Packet):
    def __init__(self, opcode: Optional[Opcodes.Friends] = None, data: Optional[FriendsPacketData] = None):
        super().__init__(id=Packets.Friends, opcode=opcode, data=data)
