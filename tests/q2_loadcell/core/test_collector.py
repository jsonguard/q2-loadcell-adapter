from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fakes import FakeConfig, FakeReactor, FakeSensor

from q2_loadcell.config import Config
from q2_loadcell.core.collector import Collector
from q2_loadcell.core.state import FastPathState

BASE = -1322000
N = 60


def _ramp():
    values: list[float] = [float(BASE + i) for i in range(N + 20)]
    values[12] = -1048585.0
    values[32] = -11.0
    values[33] = -1048585.0
    return values


class TestCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reactor = FakeReactor()

    def _make(self, fast_values=None, median_width=5, state_hz=0.0, tare=0.0):
        cfg = Config(FakeConfig({"median_width": median_width}))
        sensor = FakeSensor(fast_values=fast_values)
        state = FastPathState()
        state.hz = state_hz
        state.tare = tare
        collector = Collector(self.reactor, cfg, sensor, lambda ev: ev, state)
        return collector, sensor

    def _feed(self, collector, count=N):
        for i in range(count):
            collector._collect(i * 0.005)

    def test_start_collecting_WHEN_direct_ready_EXPECT_timer_and_sweep_rate(self):
        expected_rates = [44]
        expected_period = pytest.approx(1.0 / 250.0)
        collector, sensor = self._make(_ramp())

        collector.start_collecting()
        actual = (collector.is_started, sensor.rates, collector._sample_period)

        assert actual == (True, expected_rates, expected_period)

    def test_start_collecting_WHEN_probe_measured_hz_EXPECT_period_from_state(self):
        expected = pytest.approx(1.0 / 204.0)
        collector, _ = self._make(_ramp(), state_hz=204.0)

        collector.start_collecting()
        actual = collector._sample_period

        assert actual == expected

    def test_start_collecting_WHEN_hz_below_min_EXPECT_clamped_period(self):
        expected = pytest.approx(1.0 / 100.0)
        collector, _ = self._make(_ramp(), state_hz=50.0)

        collector.start_collecting()
        actual = collector._sample_period

        assert actual == expected

    def test_start_collecting_WHEN_direct_unavailable_EXPECT_runtime_error(self):
        expected = "query_cs1237_end_cmd"
        collector, sensor = self._make(None)

        with pytest.raises(RuntimeError) as excinfo:
            collector.start_collecting()
        actual = str(excinfo.value)

        assert expected in actual
        assert not collector.is_started
        assert sensor.rates == []

    def test_start_collecting_WHEN_sensor_missing_EXPECT_runtime_error(self):
        expected = "no sensor"
        collector, sensor = self._make(_ramp())
        sensor.fail_get = True

        with pytest.raises(RuntimeError) as excinfo:
            collector.start_collecting()
        actual = str(excinfo.value)

        assert expected in actual
        assert not collector.is_started

    def test_collect_until_WHEN_direct_samples_EXPECT_filtered_rows_and_rate_restored(self):
        expected = [[i * 0.005, 0.0, float(BASE + i), 0.0] for i in range(N)]
        collector, sensor = self._make(_ramp())
        collector.start_collecting()
        self._feed(collector)

        samples, errors = collector.collect_until(1.0)
        actual = (samples, sensor.rates)

        assert errors
        assert actual == (expected, [44, 28])

    def test_collect_until_WHEN_tare_captured_EXPECT_tare_in_column_3(self):
        expected = [111.0] * N
        collector, _ = self._make(_ramp(), tare=111.0)
        collector.start_collecting()
        self._feed(collector)

        samples, _ = collector.collect_until(1.0)
        actual = [row[3] for row in samples]

        assert actual == expected

    def test_collect_until_WHEN_median_disabled_EXPECT_corrupt_frame_kept(self):
        expected = True
        collector, _ = self._make(_ramp(), median_width=1)
        collector.start_collecting()
        self._feed(collector)

        samples, _ = collector.collect_until(1.0)
        actual = any(row[2] == -11.0 for row in samples)

        assert actual is expected

    def test_collect_until_WHEN_min_time_set_EXPECT_older_rows_dropped(self):
        expected_count = 10
        collector, _ = self._make(_ramp())
        collector.start_collecting(min_time=0.1)
        self._feed(collector, count=30)

        samples, _ = collector.collect_until(1.0)
        actual = (len(samples), all(row[0] >= 0.1 for row in samples))

        assert actual == (expected_count, True)

    def test_collect_until_WHEN_max_time_set_EXPECT_later_rows_dropped(self):
        expected_count = 21
        collector, _ = self._make(_ramp())
        collector.start_collecting()
        self._feed(collector, count=30)

        samples, _ = collector.collect_until(0.1)
        actual = (len(samples), all(row[0] <= 0.1 for row in samples))

        assert actual == (expected_count, True)

    def test_collect_until_WHEN_wait_fails_EXPECT_timer_stopped_and_rate_restored(self):
        expected = "wait failed"
        collector, sensor = self._make(_ramp())
        collector._print_time = MagicMock(side_effect=RuntimeError(expected))
        collector.start_collecting()

        with pytest.raises(RuntimeError) as excinfo:
            collector.collect_until(1.0)
        actual = str(excinfo.value)

        assert actual == expected
        assert not collector.is_started
        assert sensor.rates == [44, 28]
        assert "info: stop internal timer" in collector._logs
        assert "info: set sensor frequency to 28" in collector._logs
        assert collector._collect(1.0) == self.reactor.NEVER

    def test_collect_until_WHEN_uniform_timing_EXPECT_measured_rate(self):
        expected = pytest.approx(200.0)
        collector, _ = self._make(_ramp())
        collector.start_collecting()
        self._feed(collector, count=11)

        collector.collect_until(1.0)
        actual = collector.measured_sps

        assert actual == expected

    def test_consume_WHEN_not_started_EXPECT_reactor_never(self):
        expected = self.reactor.NEVER
        collector, _ = self._make(_ramp())

        actual = collector._collect(0.0)

        assert actual == expected

    def test_collect_until_WHEN_reads_keep_failing_EXPECT_bounded_error_list(self):
        expected_errors = 10
        expected_last = "15 more sample error(s) suppressed"
        collector, sensor = self._make(_ramp())
        sensor.fail_direct = True
        collector.start_collecting()
        self._feed(collector, count=25)

        samples, errors = collector.collect_until(1.0)
        actual = (samples, len([e for e in errors if e == "direct read failed"]), errors[-1])

        assert actual == ([], expected_errors, expected_last)
