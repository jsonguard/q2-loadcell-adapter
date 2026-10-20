from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fakes import FakeConfig

from q2_loadcell.config import Config
from q2_loadcell.hardware.sensor import Cs1237Sensor


class TestCs1237Sensor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.printer = MagicMock()
        self.gcode = MagicMock()
        self.vendor = MagicMock()
        self.vendor.oid = 5
        self.vendor.read_origin_data.return_value = -1322725
        self.printer.lookup_object.return_value = MagicMock(sensor_helper=self.vendor)
        self.cfg = Config(FakeConfig({}))
        self.sensor = Cs1237Sensor(self.printer, self.gcode, self.cfg)

    def test_get_WHEN_called_twice_EXPECT_single_lookup_and_cached_object(self):
        expected = self.vendor

        first = self.sensor.get()
        second = self.sensor.get()
        actual = (first, second)

        assert actual == (expected, expected)
        self.printer.lookup_object.assert_called_once_with("probe_air")

    def test_oid_WHEN_sensor_has_oid_EXPECT_masked_value(self):
        self.vendor.oid = 0x105
        expected = 0x05

        actual = self.sensor.oid()

        assert actual == expected

    def test_oid_WHEN_lookup_raises_EXPECT_zero(self):
        self.printer.lookup_object.side_effect = RuntimeError("boom")
        expected = 0

        actual = self.sensor.oid()

        assert actual == expected

    def test_command_WHEN_attribute_present_EXPECT_attribute_value(self):
        self.vendor.foo = "bar"
        expected = "bar"

        actual = self.sensor.command("foo")

        assert actual == expected

    def test_command_WHEN_attribute_absent_EXPECT_none(self):
        printer = MagicMock()
        printer.lookup_object.return_value = MagicMock(sensor_helper=object())
        sensor = Cs1237Sensor(printer, self.gcode, self.cfg)
        expected = None

        actual = sensor.command("missing")

        assert actual is expected

    def test_fast_wrapper_WHEN_command_sendable_EXPECT_wrapper(self):
        wrapper = MagicMock()
        self.vendor.query_cs1237_end_cmd = wrapper
        expected = wrapper

        actual = self.sensor.fast_wrapper()

        assert actual is expected

    def test_fast_wrapper_WHEN_command_absent_EXPECT_none(self):
        self.vendor.query_cs1237_end_cmd = None
        expected = None

        actual = self.sensor.fast_wrapper()

        assert actual is expected

    def test_read_vendor_WHEN_called_EXPECT_int_reading(self):
        self.vendor.read_origin_data.return_value = -1322725.0
        expected = -1322725

        actual = self.sensor.read_vendor()

        assert actual == expected

    def test_read_direct_WHEN_called_EXPECT_snapshot_of_wrapper_and_args(self):
        wrapper = MagicMock()
        wrapper.send.return_value = {"data": b"\x1b\xd1\xeb\x00"}
        self.vendor.query_cs1237_end_cmd = wrapper
        expected = -1322725

        read = self.sensor.read_direct()
        self.vendor.oid = 9  # must not affect the already-resolved closure
        actual = read()

        assert actual == expected
        wrapper.send.assert_called_once_with([5, 0, 1])

    def test_read_direct_WHEN_wrapper_absent_EXPECT_runtime_error(self):
        self.vendor.query_cs1237_end_cmd = None
        expected = "query_cs1237_end_cmd is unavailable"

        with pytest.raises(RuntimeError) as excinfo:
            self.sensor.read_direct()
        actual = str(excinfo.value)

        assert actual == expected

    def test_set_adc_rate_WHEN_ok_EXPECT_command_sent_and_none(self):
        expected = None

        actual = self.sensor.set_adc_rate(44)

        assert actual is expected
        self.gcode._process_commands.assert_called_once_with(["WEIGHTING_CONFIG_READ RATE=44"], need_ack=False)

    def test_set_adc_rate_WHEN_gcode_raises_EXPECT_error_string(self):
        self.gcode._process_commands.side_effect = RuntimeError("boom")
        expected = "44"

        actual = self.sensor.set_adc_rate(44)

        assert actual is not None
        assert expected in actual
