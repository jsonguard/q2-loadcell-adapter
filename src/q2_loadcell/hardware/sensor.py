"""
Access to the vendor CS1237 on the THR mcu (discovery, ADC rate, read paths).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol

from . import constants as C
from .decode import decode_sample

if TYPE_CHECKING:
    from gcode import GCodeDispatch
    from klippy import Printer

    from ..config import Config


class SendableCommand(Protocol):
    def send(self, data: Any = ..., minclock: int = ..., reqclock: int = ...) -> Any: ...


class Cs1237(Protocol):
    oid: int
    query_cs1237_end_cmd: SendableCommand

    def read_origin_data(self) -> int: ...


class Cs1237Sensor:
    def __init__(self, printer: Printer, gcode: GCodeDispatch, cfg: Config) -> None:
        self._printer = printer
        self._gcode = gcode
        self._cfg = cfg
        self._cache: Optional[Cs1237] = None

    def get(self) -> Cs1237:
        cache = self._cache
        if cache is None:
            probe_air = self._printer.lookup_object(C.PROBE_AIR_OBJECT)
            cache = getattr(probe_air, C.SENSOR_HELPER_ATTR)
            self._cache = cache
        return cache

    def oid(self) -> int:
        try:
            return int(getattr(self.get(), "oid", 0)) & 0xFF
        except Exception:
            return 0

    def command(self, name: str) -> Any:
        return getattr(self.get(), name, None)

    def fast_wrapper(self) -> Optional[SendableCommand]:
        wrapper = self.command(C.FAST_CMD_ATTR)
        return wrapper if _sendable(wrapper) else None

    def type_name(self) -> str:
        try:
            return type(self.get()).__name__
        except Exception:
            return "unavailable"

    def read_vendor(self) -> int:
        return int(self.get().read_origin_data())

    def read_direct(self) -> Callable[[], int]:
        wrapper = self.fast_wrapper()
        if wrapper is None:
            raise RuntimeError("query_cs1237_end_cmd is unavailable")
        args = [self.oid(), C.FAST_CMD_REG, C.FAST_CMD_LEN]

        def read() -> int:
            return decode_sample(wrapper.send(args)["data"])

        return read

    def set_adc_rate(self, code: int) -> Optional[str]:
        try:
            self._gcode._process_commands([C.WEIGHTING_CONFIG_CMD % (code,)], need_ack=False)
            return None
        except Exception as exc:
            return "set ADC rate %d failed: %s" % (code, exc)


def _sendable(wrapper: Any) -> bool:
    return callable(getattr(wrapper, "send", None))
