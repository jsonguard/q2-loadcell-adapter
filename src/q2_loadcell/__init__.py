from __future__ import annotations

from typing import TYPE_CHECKING

from .api.gcode_interface import GCodeInterface
from .api.loadcell_api import EventTimeConverter, LoadCellApi, SensorInfo
from .config import Config
from .core.collector import Collector
from .core.diagnostics import DiagnosticsCapture, DiagnosticsSettings
from .core.state import FastPathState
from .core.tare import TareCapture
from .hardware.sensor import Cs1237Sensor

if TYPE_CHECKING:
    from gcode import GCodeDispatch
    from klippy import Printer

    from .config import ConfigPort


class Q2LoadCell:
    def __init__(
        self,
        printer: Printer,
        collector: Collector,
        sensor: SensorInfo,
        api: LoadCellApi,
    ) -> None:
        self.printer = printer
        self.collector = collector
        self.sensor = sensor
        self.api = api
        self.name = "q2_loadcell"

        self.printer.register_event_handler("klippy:ready", self._handle_ready)

    def _handle_ready(self) -> None:
        # Standard discovery event used by G0BL1N/autopa.
        self.printer.send_event("load_cell:tare", self)

    def get_collector(self) -> Collector:
        return self.api.get_collector()

    def get_samples_per_second(self) -> float:
        return self.api.get_samples_per_second()


def load_config(config: ConfigPort) -> Q2LoadCell:
    printer: Printer = config.get_printer()
    reactor = printer.get_reactor()
    gcode: GCodeDispatch = printer.lookup_object("gcode")

    cfg = Config(config)
    state = FastPathState()
    hw_sensor = Cs1237Sensor(printer, gcode, cfg)
    collector = Collector(reactor, cfg, hw_sensor, EventTimeConverter(printer), state)
    api = LoadCellApi(cfg, state, collector)
    tare_capture = TareCapture(reactor, hw_sensor, state)
    diagnostics_capture = DiagnosticsCapture(
        reactor,
        hw_sensor,
        state,
        DiagnosticsSettings(median_width=cfg.median_width, spike_sigma=cfg.spike_sigma),
    )
    GCodeInterface(gcode, cfg, tare_capture, diagnostics_capture).register()

    return Q2LoadCell(
        printer=printer,
        collector=collector,
        sensor=SensorInfo(api),
        api=api,
    )
