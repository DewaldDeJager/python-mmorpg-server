from typing import Optional, Union, Dict, Any
from ..model import CamelModel
from ..packet import Packet
from ..packets import Packets
from ..opcodes import Trade as TradeOpcode

class TradeRequestData(CamelModel):
    instance: Optional[str] = None

class TradeAddData(CamelModel):
    index: int
    instance: Optional[str] = None
    count: Optional[int] = None
    key: Optional[str] = None

class TradeRemoveData(CamelModel):
    index: int
    instance: Optional[str] = None
    count: Optional[int] = None

class TradeAcceptData(CamelModel):
    message: Optional[str] = None

class TradeOpenData(CamelModel):
    instance: str

# For Close, it's a generic dict
TradePacketData = Union[TradeRequestData, TradeAddData, TradeRemoveData, TradeAcceptData, Dict[str, Any], TradeOpenData]

class TradePacket(Packet):
    def __init__(self, opcode: TradeOpcode, data: TradePacketData):
        super().__init__(id=Packets.Trade, opcode=opcode, data=data)
