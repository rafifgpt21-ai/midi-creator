"""Chunked, ASCII-only JSON over experimental-manufacturer SysEx.

Request and response directions are distinct so a shared LoopBe bus cannot echo a
response back into an executable request. No notes or CCs use the control bus.
"""

import json
import math

from .config import StudioError

PREFIX = (0x7D, 0x4D, 0x43, 1)
CHUNK_SIZE = 480
MAX_BYTES = 131072


def frames(value: dict, request_id: int, direction: int) -> list[tuple[int, ...]]:
    if type(request_id) is not int or not 1 <= request_id < 16384 or direction not in (0, 1):
        raise StudioError("Invalid bridge frame identity")
    data = json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")
    if len(data) > MAX_BYTES:
        raise StudioError("Bridge message too large")
    count = max(1, math.ceil(len(data) / CHUNK_SIZE))
    return [PREFIX + (direction, request_id & 127, request_id >> 7, index & 127, index >> 7,
                     count & 127, count >> 7) + tuple(data[index * CHUNK_SIZE:(index + 1) * CHUNK_SIZE])
            for index in range(count)]


class Assembler:
    def __init__(self, request_id: int, direction: int):
        self.request_id, self.direction = request_id, direction
        self.count = None
        self.parts = {}

    def feed(self, data) -> dict | None:
        data = tuple(data)
        if len(data) < 11 or data[:4] != PREFIX:
            return None
        direction, low, high, index_low, index_high, count_low, count_high = data[4:11]
        if direction != self.direction or low + 128 * high != self.request_id:
            return None
        index, count = index_low + 128 * index_high, count_low + 128 * count_high
        if not 1 <= count <= math.ceil(MAX_BYTES / CHUNK_SIZE) or not 0 <= index < count:
            raise StudioError("Malformed bridge chunk index")
        if self.count is not None and count != self.count:
            raise StudioError("Inconsistent bridge chunk count")
        if len(data[11:]) > CHUNK_SIZE or any(not 0 <= b < 128 for b in data[11:]):
            raise StudioError("Malformed bridge payload")
        self.count = count
        chunk = bytes(data[11:])
        if index in self.parts and self.parts[index] != chunk:
            raise StudioError("Conflicting bridge chunk")
        self.parts[index] = chunk
        if len(self.parts) != count:
            return None
        payload = b"".join(self.parts[n] for n in range(count))
        if len(payload) > MAX_BYTES:
            raise StudioError("Bridge response too large")
        try:
            result = json.loads(payload.decode("ascii"))
        except (ValueError, UnicodeError) as exc:
            raise StudioError("Invalid bridge JSON") from exc
        if not isinstance(result, dict):
            raise StudioError("Bridge response must be an object")
        return result
