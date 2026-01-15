from typing import Optional, Union
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..shared_types import HubChatPacketData

class ChatPacketData(CamelModel):
    instance: Optional[str] = None
    message: str
    with_bubble: Optional[bool] = None
    colour: Optional[str] = None
    source: Optional[str] = None

ChatData = Union[ChatPacketData, HubChatPacketData]

class ChatPacket(Packet):
    def __init__(self, data: ChatData):
        super().__init__(id=Packets.Chat, data=data)
