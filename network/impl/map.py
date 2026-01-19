import gzip
import json
import base64
from typing import Any
from network.packet import Packet
from network.packets import Packets

MapPacketData = Any

class MapPacket(Packet):
    def __init__(self, data: Any):
        # We need to handle Pydantic models in data if passed, before dumping.
        if hasattr(data, 'model_dump'):
            data = data.model_dump(mode='json', by_alias=True, exclude_none=True)

        json_str = json.dumps(data, separators=(',', ':'))
        # Using gzip.compress for compression (mimics zlib.gzipSync)
        compressed_data = gzip.compress(json_str.encode('utf-8'))
        b64_data = base64.b64encode(compressed_data).decode('utf-8')

        super().__init__(
            id=Packets.Map,
            data=b64_data,
            buffer_size=len(json_str.encode('utf-8'))
        )
