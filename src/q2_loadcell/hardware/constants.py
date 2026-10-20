from __future__ import annotations

# CS1237 output data rate selected by ``WEIGHTING_CONFIG_READ RATE=<code>``.
ADC_RATE_HZ: dict[int, float] = {28: 40.0, 44: 640.0, 60: 1280.0}

# Every response payload is a 24-bit little-endian two's-complement value
# carried in a 4-byte field.
SIGN_BYTES: int = 3

# Bound attribute names on ``probe_air.sensor_helper`` (QIDI cs1237.so).
# Names are misleading: FAST_CMD_ATTR is really the ``query_cs1237_read``
# command, while the vendor ``read_origin_data`` internally uses
# ``query_cs1237_zero``.
PROBE_AIR_OBJECT: str = "probe_air"
SENSOR_HELPER_ATTR: str = "sensor_helper"
FAST_CMD_ATTR: str = "query_cs1237_end_cmd"
FAST_CMD_REG: int = 0
FAST_CMD_LEN: int = 1
WEIGHTING_CONFIG_CMD: str = "WEIGHTING_CONFIG_READ RATE=%d"
