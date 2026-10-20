from __future__ import annotations

import array
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol

from .signal import despike_filter, measure_rate

if TYPE_CHECKING:
    from ..config import Config
    from .state import FastPathState

_MAX_RECORDED_ERRORS = 10
_COLLECT_WAIT_S = 0.2


Logs = list[str]
Measuring = list[list[float]]


class SensorPort(Protocol):
    def get(self) -> object: ...
    def read_direct(self) -> Callable[[], float]: ...
    def set_adc_rate(self, code: int) -> str | None: ...


class ReactorPort(Protocol):
    NEVER: float

    def register_timer(self, callback: Callable[[float], float], when: float) -> Any: ...
    def update_timer(self, timer_id: Any, when: float) -> None: ...
    def monotonic(self) -> float: ...
    def pause(self, when: float) -> None: ...


class Collector:
    def __init__(
        self,
        reactor: ReactorPort,
        cfg: Config,
        sensor: SensorPort,
        print_time: Callable[[float], float],
        state: FastPathState,
    ) -> None:
        self.is_started: bool = False

        self._reactor = reactor
        self._cfg = cfg
        self._sensor = sensor
        self._print_time = print_time
        self._state = state
        self._events: array.array = array.array("d")
        self._values: array.array = array.array("d")
        self._read: Optional[Callable[[], float]] = None
        self._min_time: Optional[float] = None
        self._max_time: Optional[float] = None
        self._logs: Logs = []
        self._sample_errors: int = 0
        self._sample_period: float = 1.0 / max(cfg.min_sample_hz, cfg.fallback_sample_hz)
        self.measured_sps: Optional[float] = None
        self._timer = reactor.register_timer(self._collect, reactor.NEVER)

    def start_collecting(self, min_time: Optional[float] = None) -> None:
        self._reset(min_time)

        try:
            self._read = self._sensor.read_direct()
        except Exception as exc:
            raise RuntimeError("q2_loadcell: direct register read unavailable: %s" % (exc,)) from exc
        self._sample_period = 1.0 / max(self._cfg.min_sample_hz, self._state.hz or self._cfg.fallback_sample_hz)
        self.is_started = True

        self._logs.append(f"info: set sensor frequency to {self._cfg.sweep_rate}")
        err = self._sensor.set_adc_rate(self._cfg.sweep_rate)
        if err:
            self._logs.append(f"info: {err}")

        self._logs.append(f"info: start internal timer period {self._sample_period:.6f}s")
        self._reactor.update_timer(self._timer, self._reactor.monotonic())

    def collect_until(self, print_time: float) -> tuple[Measuring, Logs]:
        self._max_time = print_time
        try:
            self._wait_until(print_time)
        finally:
            self._stop()

        samples = self._samples()
        suppressed = self._sample_errors - _MAX_RECORDED_ERRORS
        if suppressed > 0:
            self._logs.append(f"{suppressed} more sample error(s) suppressed")
        return samples, self._logs

    def _stop(self) -> None:
        self.is_started = False
        self._logs.append("info: stop internal timer")
        self._reactor.update_timer(self._timer, self._reactor.NEVER)
        self._logs.append(f"info: set sensor frequency to {self._cfg.restore_rate}")
        err = self._sensor.set_adc_rate(self._cfg.restore_rate)
        if err:
            self._logs.append(f"info: {err}")

    def _reset(self, min_time: Optional[float]) -> None:
        self._logs = []
        self._min_time = min_time
        self._max_time = None
        self.measured_sps = None
        self._events = array.array("d")
        self._values = array.array("d")
        self._sample_errors = 0

    def _collect(self, eventtime: float) -> float:
        if not self.is_started or self._read is None:
            return self._reactor.NEVER
        try:
            raw = self._read()
            self._events.append(eventtime)
            self._values.append(raw)
        except Exception as exc:
            self._sample_errors += 1
            if self._sample_errors <= _MAX_RECORDED_ERRORS:
                self._logs.append(str(exc))
        return eventtime + self._sample_period

    def _wait_until(self, print_time: float) -> None:
        while self.is_started and self._print_time(self._reactor.monotonic()) < print_time:
            self._reactor.pause(self._reactor.monotonic() + _COLLECT_WAIT_S)

    def _samples(self) -> Measuring:
        measures_count = min(len(self._events), len(self._values))
        values = despike_filter(self._values[:measures_count], self._cfg.median_width, self._cfg.spike_sigma)

        tare = self._state.tare
        result: Measuring = []

        for i in range(measures_count):
            actual_print_time = self._print_time(self._events[i])
            if self._min_time is not None and actual_print_time < self._min_time:
                continue
            if self._max_time is not None and actual_print_time > self._max_time:
                continue
            # autopa: force = -(arr[:,2] - arr[:,3]); column 1 is unused.
            result.append([actual_print_time, 0.0, float(int(values[i])), tare])

        self.measured_sps = measure_rate(result)
        return result
