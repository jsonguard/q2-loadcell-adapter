from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Protocol, Sequence

from .capture import TimerReader
from .signal import SignalStats, signal_stats

if TYPE_CHECKING:
    from .collector import ReactorPort
    from .state import FastPathState

DEFAULT_ENDSCAN_SAMPLES: int = 600
DEFAULT_ENDSCAN_OUTLIER: int = 50000
DEFAULT_MEDIAN_WIDTH: int = 5
DEFAULT_SPIKE_SIGMA: float = 6.0
DIAG_PERIOD_S: float = 0.001


class DiagnosticsSensorPort(Protocol):
    def get(self) -> Any: ...
    def set_adc_rate(self, code: int) -> str | None: ...
    def type_name(self) -> str: ...
    def read_direct(self) -> Callable[[], float]: ...


@dataclass(frozen=True)
class BenchStats:
    count: int
    samples: int
    errors: int
    mean_ms: float
    p50_ms: float
    p99_ms: float
    rate_hz: float


def calculate_bench(times: Sequence[float], done: int, errors: int, elapsed: float) -> BenchStats:
    rate_hz = done / elapsed if elapsed > 0.0 else 0.0
    if not times:
        return BenchStats(done, 0, errors, 0.0, 0.0, 0.0, rate_hz)
    ordered = sorted(times)
    return BenchStats(
        count=done,
        samples=len(ordered),
        errors=errors,
        mean_ms=1000.0 * sum(ordered) / len(ordered),
        p50_ms=1000.0 * ordered[len(ordered) // 2],
        p99_ms=1000.0 * ordered[min(len(ordered) - 1, int(len(ordered) * 0.99))],
        rate_hz=rate_hz,
    )


@dataclass(frozen=True)
class FrameScanStats:
    samples: int
    bad_frames: int
    bad_fraction: float


def calculate_frame_scan(values: Sequence[int], outlier_threshold: int) -> FrameScanStats:
    samples = len(values)
    if samples == 0:
        return FrameScanStats(0, 0, 0.0)
    median = sorted(values)[samples // 2]
    bad_frames = sum(1 for value in values if abs(value - median) > outlier_threshold)
    return FrameScanStats(samples, bad_frames, bad_frames / samples)


@dataclass(frozen=True)
class DiagnosticsSettings:
    endscan_samples: int = DEFAULT_ENDSCAN_SAMPLES
    endscan_outlier: int = DEFAULT_ENDSCAN_OUTLIER
    median_width: int = DEFAULT_MEDIAN_WIDTH
    spike_sigma: float = DEFAULT_SPIKE_SIGMA


@dataclass(frozen=True)
class DiagnosticsResult:
    sensor_type: str
    benchmark: BenchStats
    signal: SignalStats
    frame_scan: FrameScanStats | None
    scan_error: str | None


class DiagnosticsCapture:
    def __init__(
        self,
        reactor: ReactorPort,
        sensor: DiagnosticsSensorPort,
        state: FastPathState,
        settings: DiagnosticsSettings | None = None,
    ) -> None:
        self._sensor = sensor
        self._state = state
        self._settings = settings or DiagnosticsSettings()
        self._reader = TimerReader(reactor, None, DIAG_PERIOD_S)

    def capture(self, seconds: float, rate: int, restore_rate: int) -> DiagnosticsResult:
        self._sensor.get()
        sensor_type = self._sensor.type_name()
        reader = self._sensor.read_direct()
        try:
            self._sensor.set_adc_rate(rate)
            return self._capture_paths(sensor_type, seconds, reader)
        finally:
            self._sensor.set_adc_rate(restore_rate)

    def _capture_paths(
        self,
        sensor_type: str,
        seconds: float,
        read: Callable[[], float],
    ) -> DiagnosticsResult:
        fresh_s = min(seconds, 3.0)
        benchmark = self._bench(seconds, read)
        signal = self._signal(fresh_s, read)
        frame_scan, scan_error = self._scan_fast(read)
        self._state.hz = benchmark.rate_hz
        return DiagnosticsResult(sensor_type, benchmark, signal, frame_scan, scan_error)

    def _bench(self, seconds: float, read: Callable[[], float]) -> BenchStats:
        data = self._reader.run(duration_s=seconds, read=read)
        return calculate_bench(data.durations, len(data.values), data.errors, data.elapsed)

    def _signal(self, seconds: float, read: Callable[[], float]) -> SignalStats:
        data = self._reader.run(duration_s=seconds, read=read)
        return signal_stats(
            data.values,
            data.stamps,
            spike_width=self._settings.median_width,
            spike_sigma=self._settings.spike_sigma,
        )

    def _scan_fast(self, read: Callable[[], float]) -> tuple[FrameScanStats | None, str | None]:
        try:
            data = self._reader.run(count=self._settings.endscan_samples, read=read)
        except Exception as exc:
            return None, str(exc)
        if not data.values:
            return None, f"frame reads failed: {data.errors}"
        values = [int(value) for value in data.values]
        return calculate_frame_scan(values, self._settings.endscan_outlier), None
