from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol, Sequence

from .capture import TimerReader

if TYPE_CHECKING:
    from .collector import ReactorPort
    from .state import FastPathState

DEFAULT_VENDOR_PERIOD_S: float = 1.0 / 85.0


@dataclass(frozen=True)
class TareStats:
    tare: float
    noise_sigma: float
    count: int


@dataclass(frozen=True)
class TareResult:
    rate_code: int
    duration_s: float
    count: int
    effective_rate_hz: float
    errors: int
    stats: TareStats


class TareSensorPort(Protocol):
    def get(self) -> Any: ...
    def set_adc_rate(self, code: int) -> str | None: ...
    def read_vendor(self) -> int: ...


def calculate_tare(values: Sequence[float]) -> TareStats:
    count = len(values)
    if count == 0:
        return TareStats(0.0, 0.0, 0)
    tare = float(statistics.median(values))
    sigma = float(statistics.pstdev(values)) if count > 1 else 0.0
    return TareStats(tare, sigma, count)


class TareCapture:
    def __init__(
        self,
        reactor: ReactorPort,
        sensor: TareSensorPort,
        state: FastPathState,
        sample_period_s: float = DEFAULT_VENDOR_PERIOD_S,
    ) -> None:
        self._sensor = sensor
        self._state = state
        self._reader = TimerReader(reactor, sensor.read_vendor, sample_period_s)

    def capture(self, seconds: float, rate: int, restore_rate: int) -> TareResult:
        self._sensor.get()
        self._sensor.set_adc_rate(rate)
        try:
            data = self._reader.run(duration_s=seconds)
        finally:
            self._sensor.set_adc_rate(restore_rate)
        stats = calculate_tare(data.values)
        if stats.count:
            self._state.tare = stats.tare
        effective_rate_hz = stats.count / data.elapsed if data.elapsed > 0.0 else 0.0
        return TareResult(rate, seconds, stats.count, effective_rate_hz, data.errors, stats)
