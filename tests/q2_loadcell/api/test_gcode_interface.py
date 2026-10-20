from __future__ import annotations

import re
from unittest.mock import MagicMock

import pytest
from fakes import FakeConfig

from q2_loadcell.api.gcode_interface import GCodeInterface
from q2_loadcell.config import Config
from q2_loadcell.core.diagnostics import BenchStats, DiagnosticsResult, FrameScanStats
from q2_loadcell.core.signal import SignalStats
from q2_loadcell.core.tare import TareResult, TareStats


def _gcmd(seconds=0.05, rate=44):
    gcmd = MagicMock()
    gcmd.get_float.side_effect = lambda name, default=None, **kw: (
        seconds if name in ("SECONDS", "DURATION") else default
    )
    gcmd.get_int.side_effect = lambda name, default=None, **kw: rate
    gcmd.error.side_effect = lambda message: RuntimeError(message)
    return gcmd


def _signal():
    return SignalStats(
        samples=10,
        duplicates=0.0,
        stddev=1.0,
        despiked_stddev=1.0,
        outliers=0.0,
        interval_median_ms=1.0,
    )


def _diagnostics_result():
    return DiagnosticsResult(
        sensor_type="FakeSensor",
        benchmark=BenchStats(3, 3, 0, 3.0, 3.0, 4.0, 250.0),
        signal=_signal(),
        frame_scan=FrameScanStats(600, 5, 5.0 / 600.0),
        scan_error=None,
    )


class TestGCodeInterface:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.gcode = MagicMock()
        self.cfg = Config(FakeConfig({}))
        self.tare_capture = MagicMock()
        self.diagnostics_capture = MagicMock()
        self.iface = GCodeInterface(
            self.gcode,
            self.cfg,
            self.tare_capture,
            self.diagnostics_capture,
        )

    def test_register_WHEN_called_EXPECT_two_commands_registered(self):
        expected = 2

        self.iface.register()
        actual = self.gcode.register_command.call_count

        assert actual == expected

    def test_register_WHEN_called_EXPECT_q_command_names(self):
        expected = ["Q_LOADCELL_PROBE", "Q_LOADCELL_DEBUG"]

        self.iface.register()
        actual = [call.args[0] for call in self.gcode.register_command.call_args_list]

        assert actual == expected

    def test_register_WHEN_called_EXPECT_names_supported_by_klipper_parser(self):
        expected = True

        self.iface.register()
        names = [call.args[0] for call in self.gcode.register_command.call_args_list]
        actual = all(re.fullmatch(r"[A-Z_]+", name) for name in names)

        assert actual is expected

    def test__emit_WHEN_ten_lines_EXPECT_two_chunks(self):
        gcmd = MagicMock()
        lines = ["l%d" % i for i in range(10)]
        expected = ["\n".join(lines[:8]), "\n".join(lines[8:])]

        GCodeInterface._emit(gcmd, lines)
        actual = [call.args[0] for call in gcmd.respond_info.call_args_list]

        assert actual == expected

    def test_cmd_Q_LOADCELL_PROBE_WHEN_available_EXPECT_tare_report(self):
        gcmd = _gcmd(seconds=0.05)
        self.tare_capture.capture.return_value = TareResult(
            rate_code=44,
            duration_s=0.05,
            count=3,
            effective_rate_hz=60.0,
            errors=0,
            stats=TareStats(111.0, 2.0, 3),
        )
        expected = "q2_loadcell tare capture"

        self.iface.cmd_Q_LOADCELL_PROBE(gcmd)
        report = gcmd.respond_info.call_args.args[0]
        actual = report.splitlines()[0]

        assert actual == expected
        self.tare_capture.capture.assert_called_once_with(0.05, 44, self.cfg.restore_rate)
        assert "median tare: 111.0 counts" in report
        assert "noise sigma: 2.00 counts" in report

    def test_cmd_Q_LOADCELL_PROBE_WHEN_sensor_missing_EXPECT_error(self):
        self.tare_capture.capture.side_effect = RuntimeError("no sensor")
        gcmd = _gcmd()
        expected = "probe_air sensor unavailable"

        with pytest.raises(RuntimeError) as excinfo:
            self.iface.cmd_Q_LOADCELL_PROBE(gcmd)
        actual = str(excinfo.value)

        assert expected in actual

    def test_cmd_Q_LOADCELL_DEBUG_WHEN_available_EXPECT_diagnostics(self):
        gcmd = _gcmd()
        self.diagnostics_capture.capture.return_value = _diagnostics_result()
        expected = [
            "q2_loadcell diagnostics",
            "type: FakeSensor",
            "rate: 250.0 Hz",
            "bad frames: 5 (0.83 %)",
        ]

        self.iface.cmd_Q_LOADCELL_DEBUG(gcmd)
        actual = "\n".join(call.args[0] for call in gcmd.respond_info.call_args_list)

        for fragment in expected:
            assert fragment in actual

    def test_cmd_Q_LOADCELL_DEBUG_WHEN_sensor_missing_EXPECT_message(self):
        self.diagnostics_capture.capture.side_effect = RuntimeError("no sensor")
        gcmd = _gcmd()
        expected = "error: no sensor"

        self.iface.cmd_Q_LOADCELL_DEBUG(gcmd)
        actual = "\n".join(call.args[0] for call in gcmd.respond_info.call_args_list)

        assert expected in actual
