from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fakes import FakeConfig, FakeReactor

from q2_loadcell import Q2LoadCell, load_config
from q2_loadcell.api.loadcell_api import SensorInfo
from q2_loadcell.core.collector import Collector


class TestQ2LoadCell:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.printer = MagicMock()
        self.collector = MagicMock()
        self.sensor = MagicMock()
        self.api = MagicMock()
        self.lc = Q2LoadCell(
            printer=self.printer,
            collector=self.collector,
            sensor=self.sensor,
            api=self.api,
        )

    def test___init___WHEN_constructed_EXPECT_event_registered(self):
        expected = "q2_loadcell"

        actual = self.lc.name

        assert actual == expected
        self.printer.register_event_handler.assert_called_once_with("klippy:ready", self.lc._handle_ready)

    def test_get_collector_WHEN_called_EXPECT_api_collector(self):
        expected = self.api.get_collector.return_value

        actual = self.lc.get_collector()

        assert actual is expected

    def test_get_samples_per_second_WHEN_called_EXPECT_api_rate(self):
        expected = 204.0
        self.api.get_samples_per_second.return_value = expected

        actual = self.lc.get_samples_per_second()

        assert actual == expected

    def test__handle_ready_WHEN_called_EXPECT_tare_event_sent(self):
        expected = ("load_cell:tare", self.lc)

        self.lc._handle_ready()
        actual = self.printer.send_event.call_args.args

        assert actual == expected


class TestLoadConfig:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reactor = FakeReactor()
        self.gcode = MagicMock()
        self.printer = MagicMock()
        self.printer.get_reactor.return_value = self.reactor
        self.printer.lookup_object.return_value = self.gcode
        self.config = FakeConfig({}, printer=self.printer)

    def test_load_config_WHEN_called_EXPECT_wired_loadcell_and_commands(self):
        expected = {
            "name": "q2_loadcell",
            "collector": Collector,
            "sensor": SensorInfo,
            "commands": ["Q_LOADCELL_PROBE", "Q_LOADCELL_DEBUG"],
        }

        lc = load_config(self.config)
        actual = {
            "name": lc.name,
            "collector": type(lc.collector),
            "sensor": type(lc.sensor),
            "commands": [call.args[0] for call in self.gcode.register_command.call_args_list],
        }

        assert isinstance(lc, Q2LoadCell)
        assert actual == expected
