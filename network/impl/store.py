from typing import List, Optional
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Store as StoreOpcode

class SerializedStoreItem(CamelModel):
    key: str
    name: str
    count: int
    price: int
    index: Optional[int] = None

class StorePacketData(CamelModel):
    key: Optional[str] = None
    currency: Optional[str] = None
    item: Optional[SerializedStoreItem] = None
    items: Optional[List[SerializedStoreItem]] = None

class StorePacket(Packet):
    def __init__(self, opcode: StoreOpcode, data: StorePacketData):
        super().__init__(id=Packets.Store, opcode=opcode, data=data)
