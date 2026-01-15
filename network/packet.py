from typing import Any, Optional, List
from enum import IntEnum
from pydantic import BaseModel, ConfigDict
from .packets import Packets

class Packet(BaseModel):
    id: Packets
    opcode: Optional[IntEnum] = None
    data: Optional[Any] = None
    buffer_size: Optional[int] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def serialize(self) -> List[Any]:
        """
        Serializes the packet into a list format expected by the client.
        Format: [id, data] or [id, opcode, data] + [buffer_size] (optional)
        """
        packet_id = self.id.value
        opcode_val = self.opcode.value if self.opcode is not None else None

        data_val = self.data
        if isinstance(data_val, BaseModel):
            # Serialize Pydantic models to dict, ensuring aliases (camelCase) are used
            # and None values are excluded (similar to TS ignoring undefined)
            data_val = data_val.model_dump(by_alias=True, exclude_none=True)
        elif isinstance(data_val, list):
             data_val = [item.model_dump(by_alias=True, exclude_none=True) if isinstance(item, BaseModel) else item for item in data_val]

        if opcode_val is None:
            packet = [packet_id, data_val]
        else:
            packet = [packet_id, opcode_val, data_val]

        if self.buffer_size:
            packet.append(self.buffer_size)

        return packet
