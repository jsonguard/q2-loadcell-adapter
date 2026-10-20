from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gcode import GCodeCommand, GCodeDispatch

    from ..config import Config
    from ..core.diagnostics import BenchStats, DiagnosticsCapture, DiagnosticsResult
    from ..core.signal import SignalStats
    from ..core.tare import TareCapture, TareResult

_DEFAULT_PROBE_SECONDS: float = 3.0
_DEFAULT_DEBUG_SECONDS: float = 5.0


class GCodeInterface:
    def __init__(
        self,
        gcode: GCodeDispatch,
        cfg: Config,
        tare_capture: TareCapture,
        diagnostics_capture: DiagnosticsCapture,
    ) -> None:
        self._gcode = gcode
        self._cfg = cfg
        self._tare_capture = tare_capture
        self._diagnostics_capture = diagnostics_capture

    def register(self) -> None:
        self._gcode.register_command(
            "Q_LOADCELL_PROBE",
            self.cmd_Q_LOADCELL_PROBE,
            desc="Read and store the load-cell baseline/tare without moving the printer",
        )
        self._gcode.register_command(
            "Q_LOADCELL_DEBUG",
            self.cmd_Q_LOADCELL_DEBUG,
            desc="Diagnostic dump of the CS1237 interface, rates and frame quality",
        )

    def cmd_Q_LOADCELL_PROBE(self, gcmd: GCodeCommand) -> None:
        seconds = gcmd.get_float("SECONDS", gcmd.get_float("DURATION", _DEFAULT_PROBE_SECONDS), minval=0.5, maxval=30.0)
        rate = gcmd.get_int("RATE", self._cfg.sweep_rate, minval=28, maxval=60)

        self._emit(gcmd, [f"q2_loadcell started SECONDS={seconds} RATE={rate}"])

        try:
            result = self._tare_capture.capture(seconds, rate, self._cfg.restore_rate)
        except Exception as exc:
            raise gcmd.error("q2_loadcell: probe_air sensor unavailable: %s" % (exc,)) from exc

        self._emit(gcmd, self._format_tare(result))

    def cmd_Q_LOADCELL_DEBUG(self, gcmd: GCodeCommand) -> None:
        seconds = gcmd.get_float("SECONDS", _DEFAULT_DEBUG_SECONDS, minval=0.5, maxval=30.0)
        rate = gcmd.get_int("RATE", self._cfg.sweep_rate, minval=28, maxval=60)

        self._emit(gcmd, [f"q2_loadcell started SECONDS={seconds} RATE={rate}"])

        try:
            result = self._diagnostics_capture.capture(seconds, rate, self._cfg.restore_rate)
        except Exception as exc:
            self._emit(gcmd, ["q2_loadcell diagnostics", "  error: %s" % (exc,)])
            return
        self._emit(gcmd, self._format_probe(result))

    @staticmethod
    def _format_tare(result: TareResult) -> list[str]:
        lines = [
            "q2_loadcell tare capture",
            "  rate code: %d" % (result.rate_code,),
            "  duration: %.3f s" % (result.duration_s,),
            "  samples: %d" % (result.count,),
            "  effective rate: %.2f Hz" % (result.effective_rate_hz,),
            "  errors: %d" % (result.errors,),
        ]
        if result.count:
            lines.append("  median tare: %.1f counts" % (result.stats.tare,))
            lines.append("  noise sigma: %.2f counts" % (result.stats.noise_sigma,))
        else:
            lines.append("  median tare: not available")
        return lines

    @staticmethod
    def _format_probe(result: DiagnosticsResult) -> list[str]:
        lines = [
            "q2_loadcell diagnostics",
            "  interface",
            "    type: %s" % (result.sensor_type,),
            "  rate benchmark",
        ]
        lines.extend(GCodeInterface._format_bench(result.benchmark))
        lines.append("  signal quality")
        lines.extend(GCodeInterface._format_signal(result.signal))
        lines.append("  frame integrity")
        if result.scan_error is not None:
            lines.append("    error: %s" % (result.scan_error,))
        elif result.frame_scan is not None:
            lines.append("    samples: %d" % (result.frame_scan.samples,))
            lines.append(
                "    bad frames: %d (%.2f %%)" % (result.frame_scan.bad_frames, result.frame_scan.bad_fraction * 100.0)
            )
        return lines

    @staticmethod
    def _format_bench(stats: BenchStats) -> list[str]:
        return [
            "    successful reads: %d" % (stats.count,),
            "    errors: %d" % (stats.errors,),
            "    rate: %.1f Hz" % (stats.rate_hz,),
            "    latency mean/p50/p99: %.3f / %.3f / %.3f ms" % (stats.mean_ms, stats.p50_ms, stats.p99_ms),
        ]

    @staticmethod
    def _format_signal(stats: SignalStats) -> list[str]:
        return [
            "    samples: %d" % (stats.samples,),
            "    duplicates: %.2f %%" % (stats.duplicates * 100.0,),
            "    standard deviation: %.2f counts" % (stats.stddev,),
            "    after despiking: %.2f counts" % (stats.despiked_stddev,),
            "    outliers replaced: %.2f %%" % (stats.outliers * 100.0,),
            "    median interval: %.2f ms" % (stats.interval_median_ms,),
        ]

    @staticmethod
    def _emit(gcmd: GCodeCommand, lines: list[str]) -> None:
        for i in range(0, len(lines), 8):
            gcmd.respond_info("\n".join(lines[i : i + 8]))
