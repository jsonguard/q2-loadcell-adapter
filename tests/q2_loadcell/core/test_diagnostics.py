from __future__ import annotations

import pytest
from fakes import FakeSensor, FakeTimerReactor

from q2_loadcell.core.diagnostics import (
    DiagnosticsCapture,
    DiagnosticsSettings,
    calculate_bench,
    calculate_frame_scan,
)
from q2_loadcell.core.state import FastPathState


class TestDiagnostics:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.times = [0.001, 0.003, 0.002]
        self.frame_values = [100] * 10 + [100000]

    def test_calculate_bench_WHEN_times_EXPECT_rate_and_percentiles(self):
        expected = {
            "count": 3,
            "samples": 3,
            "errors": 1,
            "mean_ms": pytest.approx(2.0),
            "p50_ms": pytest.approx(2.0),
            "p99_ms": pytest.approx(3.0),
            "rate_hz": pytest.approx(300.0),
        }

        stats = calculate_bench(self.times, done=3, errors=1, elapsed=0.01)
        actual = {
            "count": stats.count,
            "samples": stats.samples,
            "errors": stats.errors,
            "mean_ms": stats.mean_ms,
            "p50_ms": stats.p50_ms,
            "p99_ms": stats.p99_ms,
            "rate_hz": stats.rate_hz,
        }

        assert actual == expected

    def test_calculate_bench_WHEN_no_times_EXPECT_no_timing(self):
        expected = {"samples": 0, "errors": 2, "rate_hz": 0.0}

        stats = calculate_bench([], done=0, errors=2, elapsed=0.5)
        actual = {"samples": stats.samples, "errors": stats.errors, "rate_hz": stats.rate_hz}

        assert actual == expected

    def test_calculate_frame_scan_WHEN_outlier_EXPECT_bad_fraction(self):
        expected = {
            "samples": 11,
            "bad_frames": 1,
            "bad_fraction": pytest.approx(1.0 / 11.0),
        }

        stats = calculate_frame_scan(self.frame_values, outlier_threshold=50000)
        actual = {
            "samples": stats.samples,
            "bad_frames": stats.bad_frames,
            "bad_fraction": stats.bad_fraction,
        }

        assert actual == expected


class TestDiagnosticsCapture:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reactor = FakeTimerReactor()
        self.sensor = FakeSensor(fast_values=[111], vendor_value=111)
        self.state = FastPathState()
        self.capture = DiagnosticsCapture(
            self.reactor,
            self.sensor,
            self.state,
            DiagnosticsSettings(endscan_samples=10),
        )

    def test_capture_WHEN_sensor_available_EXPECT_result_and_state(self):
        expected = ("FakeSensor", True, True, 10, None, [44, 28])

        result = self.capture.capture(0.05, 44, 28)
        actual = (
            result.sensor_type,
            result.benchmark.rate_hz > 0.0,
            result.signal.samples >= 0,
            result.frame_scan.samples if result.frame_scan is not None else None,
            result.scan_error,
            self.sensor.rates,
        )

        assert actual == expected
        assert self.state.hz == result.benchmark.rate_hz

    def test_capture_WHEN_available_EXPECT_readers_snapshotted_before_rate(self):
        expected = ["read_direct", "rate:44"]

        self.capture.capture(0.05, 44, 28)
        actual = self.sensor.events[:2]

        assert actual == expected

    def test_capture_WHEN_sensor_missing_EXPECT_error(self):
        expected = "no sensor"
        self.sensor.fail_get = True

        with pytest.raises(RuntimeError) as excinfo:
            self.capture.capture(0.05, 44, 28)
        actual = str(excinfo.value)

        assert actual == expected
