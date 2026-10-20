from __future__ import annotations

import pytest
from fakes import FakeSensor, FakeTimerReactor

from q2_loadcell.core.state import FastPathState
from q2_loadcell.core.tare import TareCapture, calculate_tare


class TestTare:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.values = [1.0, 2.0, 3.0]

    def test_calculate_tare_WHEN_empty_EXPECT_zero_stats(self):
        expected = (0.0, 0.0, 0)

        stats = calculate_tare([])
        actual = (stats.tare, stats.noise_sigma, stats.count)

        assert actual == expected

    def test_calculate_tare_WHEN_single_sample_EXPECT_zero_noise(self):
        expected = (111.0, 0.0, 1)

        stats = calculate_tare([111.0])
        actual = (stats.tare, stats.noise_sigma, stats.count)

        assert actual == expected

    def test_calculate_tare_WHEN_samples_EXPECT_median_and_sigma(self):
        expected = {"tare": 2.0, "noise_sigma": pytest.approx(0.8164965809), "count": 3}

        stats = calculate_tare(self.values)
        actual = {"tare": stats.tare, "noise_sigma": stats.noise_sigma, "count": stats.count}

        assert actual == expected


class TestTareCapture:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reactor = FakeTimerReactor()
        self.sensor = FakeSensor(vendor_value=111)
        self.state = FastPathState()
        self.capture = TareCapture(self.reactor, self.sensor, self.state)

    def test_capture_WHEN_sensor_available_EXPECT_tare_and_rate_restore(self):
        expected = (True, 111.0, True, 111.0, [44, 28])

        result = self.capture.capture(0.05, 44, 28)
        actual = (
            result.count > 0,
            result.stats.tare,
            result.effective_rate_hz > 0.0,
            self.state.tare,
            self.sensor.rates,
        )

        assert actual == expected

    def test_capture_WHEN_sensor_missing_EXPECT_error(self):
        expected = "no sensor"
        self.sensor.fail_get = True

        with pytest.raises(RuntimeError) as excinfo:
            self.capture.capture(0.05, 44, 28)
        actual = str(excinfo.value)

        assert actual == expected

    def test_capture_WHEN_reads_fail_EXPECT_empty_result_and_restored_rate(self):
        expected = (0, True, 0.0, [44, 28])
        self.sensor.fail_vendor = True

        result = self.capture.capture(0.05, 44, 28)
        actual = (result.count, result.errors > 0, self.state.tare, self.sensor.rates)

        assert actual == expected
