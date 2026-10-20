from . import bus as bus
from _typeshed import Incomplete

REPLICAPE_MAX_CURRENT: float
REPLICAPE_PCA9685_BUS: int
REPLICAPE_PCA9685_ADDRESS: int
REPLICAPE_PCA9685_CYCLE_TIME: float
PIN_MIN_TIME: float

class pca9685_pwm:
    _replicape: Incomplete
    _channel: Incomplete
    _mcu: Incomplete
    _reactor: Incomplete
    _bus: Incomplete
    _address: Incomplete
    _cycle_time: Incomplete
    _max_duration: float
    _oid: Incomplete
    _invert: Incomplete
    _start_value: Incomplete
    _is_enable: Incomplete
    _last_clock: int
    _pwm_max: float
    _set_cmd: Incomplete
    def __init__(self, replicape, channel, pin_type, pin_params) -> None: ...
    def get_mcu(self): ...
    def setup_max_duration(self, max_duration) -> None: ...
    def setup_cycle_time(self, cycle_time, hardware_pwm: bool = False) -> None: ...
    _shutdown_value: Incomplete
    def setup_start_value(self, start_value, shutdown_value) -> None: ...
    def _build_config(self) -> None: ...
    def set_pwm(self, print_time, value): ...
    def set_digital(self, print_time, value) -> None: ...

class ReplicapeDACEnable:
    mcu: Incomplete
    value: Incomplete
    pwm: Incomplete
    def __init__(self, replicape, channel, pin_type, pin_params) -> None: ...
    def get_mcu(self): ...
    def setup_max_duration(self, max_duration) -> None: ...
    def set_digital(self, print_time, value) -> None: ...

SERVO_PINS: Incomplete

class servo_pwm:
    mcu_pwm: Incomplete
    get_mcu: Incomplete
    setup_max_duration: Incomplete
    setup_start_value: Incomplete
    set_pwm: Incomplete
    def __init__(self, replicape, pin_params) -> None: ...
    def setup_cycle_time(self, cycle_time, hardware_pwm: bool = False) -> None: ...

ReplicapeStepConfig: Incomplete

class Replicape:
    host_mcu: Incomplete
    mcu_pwm_enable: Incomplete
    mcu_pwm_start_value: bool
    last_pwm_enable_time: float
    pins: Incomplete
    servo_pins: Incomplete
    stepper_dacs: Incomplete
    enabled_channels: Incomplete
    sr_disabled: Incomplete
    sr_enabled: Incomplete
    sr_spi: Incomplete
    def __init__(self, config) -> None: ...
    def note_pwm_start_value(self, channel, start_value, shutdown_value) -> None: ...
    def note_pwm_enable(self, print_time, channel, is_enable) -> None: ...
    def setup_pin(self, pin_type, pin_params): ...

def load_config(config): ...
