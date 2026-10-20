from . import filament_switch_sensor as filament_switch_sensor
from _typeshed import Incomplete

ADC_REPORT_TIME: float
ADC_SAMPLE_TIME: float
ADC_SAMPLE_COUNT: int

class HallFilamentWidthSensor:
    printer: Incomplete
    reactor: Incomplete
    pin1: Incomplete
    pin2: Incomplete
    dia1: Incomplete
    dia2: Incomplete
    rawdia1: Incomplete
    rawdia2: Incomplete
    MEASUREMENT_INTERVAL_MM: Incomplete
    nominal_filament_dia: Incomplete
    measurement_delay: Incomplete
    measurement_max_difference: Incomplete
    max_diameter: Incomplete
    min_diameter: Incomplete
    diameter: Incomplete
    is_active: Incomplete
    runout_dia_min: Incomplete
    runout_dia_max: Incomplete
    is_log: Incomplete
    use_current_dia_while_delay: Incomplete
    filament_array: Incomplete
    lastFilamentWidthReading: int
    lastFilamentWidthReading2: int
    firstExtruderUpdatePosition: int
    filament_width: Incomplete
    toolhead: Incomplete
    ppins: Incomplete
    mcu_adc: Incomplete
    mcu_adc2: Incomplete
    extrude_factor_update_timer: Incomplete
    gcode: Incomplete
    runout_helper: Incomplete
    def __init__(self, config) -> None: ...
    def handle_ready(self) -> None: ...
    def adc_callback(self, read_time, read_value) -> None: ...
    def adc2_callback(self, read_time, read_value) -> None: ...
    def update_filament_array(self, last_epos) -> None: ...
    def extrude_factor_update_event(self, eventtime): ...
    def cmd_M407(self, gcmd) -> None: ...
    def cmd_ClearFilamentArray(self, gcmd) -> None: ...
    def cmd_M405(self, gcmd) -> None: ...
    def cmd_M406(self, gcmd) -> None: ...
    def cmd_Get_Raw_Values(self, gcmd) -> None: ...
    def get_status(self, eventtime): ...
    def cmd_log_enable(self, gcmd) -> None: ...
    def cmd_log_disable(self, gcmd) -> None: ...

def load_config(config): ...
