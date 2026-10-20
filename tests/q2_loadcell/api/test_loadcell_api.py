from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fakes import FakeConfig

from q2_loadcell.api.loadcell_api import EventTimeConverter, LoadCellApi, SensorInfo
from q2_loadcell.config import Config
from q2_loadcell.core.state import FastPathState


class TestPrintTime:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.printer = MagicMock()
        self.mcu = MagicMock()
        self.mcu.estimated_print_time.return_value = 12.5
        self.printer.lookup_object.return_value = self.mcu
        self.clock = EventTimeConverter(self.printer)

    def test___call___WHEN_first_call_EXPECT_mcu_lookup_and_print_time(self):
        expected = 12.5

        actual = self.clock(100.0)

        assert actual == expected
        self.mcu.estimated_print_time.assert_called_once_with(100.0)

    def test___call___WHEN_called_again_EXPECT_mcu_lookup_cached(self):
        expected = 1

        self.clock(100.0)
        self.clock(101.0)
        actual = self.printer.lookup_object.call_count

        assert actual == expected
        self.printer.lookup_object.assert_called_once_with("mcu")


class TestSensorInfo:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = MagicMock()
        self.api.get_samples_per_second.return_value = 204.0
        self.info = SensorInfo(self.api)

    def test_get_samples_per_second_WHEN_called_EXPECT_api_value(self):
        expected = 204.0

        actual = self.info.get_samples_per_second()

        assert actual == expected


class TestLoadCellApi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.cfg = Config(FakeConfig({}))
        self.state = FastPathState()
        self.collector = MagicMock()
        self.api = LoadCellApi(self.cfg, self.state, self.collector)

    def test_get_collector_WHEN_called_EXPECT_wrapped_collector(self):
        expected = self.collector

        actual = self.api.get_collector()

        assert actual is expected

    def test_get_samples_per_second_WHEN_measured_EXPECT_measured_rate(self):
        expected = 204.0
        self.collector.measured_sps = expected

        actual = self.api.get_samples_per_second()

        assert actual == expected

    def test_get_samples_per_second_WHEN_not_measured_EXPECT_probe_rate(self):
        expected = 270.0
        self.collector.measured_sps = None
        self.state.hz = expected

        actual = self.api.get_samples_per_second()

        assert actual == expected

    def test_get_samples_per_second_WHEN_no_probe_rate_EXPECT_adc_rate_fallback(self):
        expected = 640.0
        self.collector.measured_sps = None
        self.state.hz = 0.0

        actual = self.api.get_samples_per_second()

        assert actual == expected
