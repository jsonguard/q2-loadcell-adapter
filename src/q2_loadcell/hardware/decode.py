from __future__ import annotations

from .constants import SIGN_BYTES


def decode_sample(payload: bytes | bytearray, sign_bytes: int = SIGN_BYTES) -> int:
    """24-bit little-endian two's-complement payload to signed int (e.g.
    ``0xEBD11B`` -> -1322725, not +15.4e6; the 4th byte is padding)."""
    return int.from_bytes(payload[:sign_bytes], "little", signed=True)
