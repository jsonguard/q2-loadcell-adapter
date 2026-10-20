from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..core.collector import Collector
from ..core.state import FastPathState
from ..hardware.constants import ADC_RATE_HZ

if TYPE_CHECKING:
    from klippy import Printer
    from mcu import MCU

    from ..config import Config


class EventTimeConverter:
    def __init__(self, printer: Printer) -> None:
        self._printer = printer
        self._mcu: Optional[MCU] = None

    def __call__(self, eventtime: float) -> float:
        mcu = self._mcu
        if mcu is None:
            mcu = self._printer.lookup_object("mcu")
            self._mcu = mcu
        return mcu.estimated_print_time(eventtime)


class SensorInfo:
    def __init__(self, api: "LoadCellApi") -> None:
        self._api = api

    def get_samples_per_second(self) -> float:
        return self._api.get_samples_per_second()


class LoadCellApi:
    def __init__(self, cfg: Config, state: FastPathState, collector: Collector) -> None:
        self._cfg = cfg
        self._state = state
        self._collector = collector

    def get_collector(self) -> Collector:
        return self._collector

    def get_samples_per_second(self) -> float:
        return self._collector.measured_sps or self._state.hz or ADC_RATE_HZ.get(self._cfg.sweep_rate, 640.0)
