from typing import List, Optional, Dict
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Store as StoreOpcode

class StoreItem(CamelModel):
    key: str
    count: int
    price: Optional[int] = None
    stock_amount: Optional[int] = None

class StoreData(CamelModel):
    items: List[StoreItem]
    refresh: int
    currency: str
    restricted: Optional[bool] = None

RawStore = Dict[str, StoreData]

class SerializedStoreItem(CamelModel):
    key: str
    name: str
    count: int
    price: int
    index: Optional[int] = None

class StorePacketData(CamelModel):
    key: Optional[str] = None
    currency: Optional[str] = None
    item: Optional[SerializedStoreItem] = None  # Used for selecting items.
    items: Optional[List[SerializedStoreItem]] = None  # Used for batch data.

class StorePacket(Packet):
    def __init__(self, opcode: StoreOpcode, data: StorePacketData):
        super().__init__(id=Packets.Store, opcode=opcode, data=data)
