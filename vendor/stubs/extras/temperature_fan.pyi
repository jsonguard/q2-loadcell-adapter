from . import fan as fan
from _typeshed import Incomplete

KELVIN_TO_CELSIUS: float
MAX_FAN_TIME: float
AMBIENT_TEMP: float
PID_PARAM_BASE: float

class TemperatureFan:
    name: Incomplete
    printer: Incomplete
    fan: Incomplete
    min_temp: Incomplete
    max_temp: Incomplete
    sensor: Incomplete
    speed_delay: Incomplete
    max_speed_conf: Incomplete
    max_speed: Incomplete
    min_speed_conf: Incomplete
    min_speed: Incomplete
    last_temp: float
    last_temp_time: float
    target_temp_conf: Incomplete
    target_temp: Incomplete
    control: Incomplete
    next_speed_time: float
    last_speed_value: float
    def __init__(self, config) -> None: ...
    def set_speed(self, read_time, value) -> None: ...
    def temperature_callback(self, read_time, temp) -> None: ...
    def get_temp(self, eventtime): ...
    def get_min_speed(self): ...
    def get_max_speed(self): ...
    def get_status(self, eventtime): ...
    cmd_SET_TEMPERATURE_FAN_TARGET_help: str
    def cmd_SET_TEMPERATURE_FAN_TARGET(self, gcmd) -> None: ...
    def set_temp(self, degrees) -> None: ...
    def set_min_speed(self, speed) -> None: ...
    def set_max_speed(self, speed) -> None: ...

class ControlBangBang:
    temperature_fan: Incomplete
    max_delta: Incomplete
    heating: bool
    def __init__(self, temperature_fan, config) -> None: ...
    def temperature_callback(self, read_time, temp) -> None: ...

PID_SETTLE_DELTA: float
PID_SETTLE_SLOPE: float

class ControlPID:
    temperature_fan: Incomplete
    Kp: Incomplete
    Ki: Incomplete
    Kd: Incomplete
    min_deriv_time: Incomplete
    temp_integ_max: float
    prev_temp: Incomplete
    prev_temp_time: float
    prev_temp_deriv: float
    prev_temp_integ: float
    def __init__(self, temperature_fan, config) -> None: ...
    def temperature_callback(self, read_time, temp) -> None: ...

def load_config_prefix(config): ...
