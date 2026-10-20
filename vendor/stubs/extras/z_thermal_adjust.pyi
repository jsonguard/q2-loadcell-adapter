from _typeshed import Incomplete

KELVIN_TO_CELSIUS: float

class ZThermalAdjuster:
    printer: Incomplete
    gcode: Incomplete
    lock: Incomplete
    config: Incomplete
    temp_coeff: Incomplete
    off_above_z: Incomplete
    max_z_adjust_mm: Incomplete
    smooth_time: Incomplete
    inv_smooth_time: Incomplete
    min_temp: Incomplete
    max_temp: Incomplete
    sensor: Incomplete
    last_temp: float
    measured_min: float
    smoothed_temp: float
    last_temp_time: float
    ref_temperature: float
    ref_temp_override: bool
    z_adjust_mm: float
    last_z_adjust_mm: float
    adjust_enable: bool
    last_position: Incomplete
    next_transform: Incomplete
    def __init__(self, config) -> None: ...
    toolhead: Incomplete
    z_step_dist: Incomplete
    def handle_connect(self) -> None: ...
    def get_status(self, eventtime): ...
    def handle_homing_move_end(self, homing_state, rails) -> None: ...
    def calc_adjust(self, pos): ...
    def calc_unadjust(self, pos): ...
    def get_position(self): ...
    def move(self, newpos, speed) -> None: ...
    measured_max: Incomplete
    def temperature_callback(self, read_time, temp) -> None: ...
    def get_temp(self, eventtime): ...
    def stats(self, eventtime): ...
    def cmd_SET_Z_THERMAL_ADJUST(self, gcmd) -> None: ...
    cmd_SET_Z_THERMAL_ADJUST_help: str

def load_config(config): ...
