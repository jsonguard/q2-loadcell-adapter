from _typeshed import Incomplete

ADC_REPORT_TIME: float
ADC_SAMPLE_TIME: float
ADC_SAMPLE_COUNT: int
MEASUREMENT_INTERVAL_MM: int

class FilamentWidthSensor:
    printer: Incomplete
    reactor: Incomplete
    pin: Incomplete
    nominal_filament_dia: Incomplete
    measurement_delay: Incomplete
    measurement_max_difference: Incomplete
    max_diameter: Incomplete
    min_diameter: Incomplete
    is_active: bool
    filament_array: Incomplete
    lastFilamentWidthReading: int
    toolhead: Incomplete
    ppins: Incomplete
    mcu_adc: Incomplete
    extrude_factor_update_timer: Incomplete
    gcode: Incomplete
    def __init__(self, config) -> None: ...
    def handle_ready(self) -> None: ...
    def adc_callback(self, read_time, read_value) -> None: ...
    def update_filament_array(self, last_epos) -> None: ...
    def extrude_factor_update_event(self, eventtime): ...
    def cmd_M407(self, gcmd) -> None: ...
    def cmd_ClearFilamentArray(self, gcmd) -> None: ...
    def cmd_M405(self, gcmd) -> None: ...
    def cmd_M406(self, gcmd) -> None: ...

def load_config(config): ...
