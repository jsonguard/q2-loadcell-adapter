from _typeshed import Incomplete

PIN_MIN_TIME: float
MAX_SCHEDULE_TIME: float

class MCU_pwm_cycle:
    _mcu: Incomplete
    _cycle_time: Incomplete
    _oid: Incomplete
    _pin: Incomplete
    _invert: Incomplete
    _start_value: Incomplete
    _shutdown_value: Incomplete
    _last_clock: int
    _set_cmd: Incomplete
    def __init__(self, pin_params, cycle_time, start_value, shutdown_value) -> None: ...
    _cycle_ticks: Incomplete
    _set_cycle_ticks: Incomplete
    def _build_config(self) -> None: ...
    def set_pwm_cycle(self, print_time, value, cycle_time) -> None: ...

class PrinterOutputPWMCycle:
    printer: Incomplete
    last_print_time: float
    last_cycle_time: Incomplete
    scale: Incomplete
    last_value: Incomplete
    shutdown_value: Incomplete
    mcu_pin: Incomplete
    def __init__(self, config) -> None: ...
    def get_status(self, eventtime): ...
    def _set_pin(self, print_time, value, cycle_time) -> None: ...
    cmd_SET_PIN_help: str
    def cmd_SET_PIN(self, gcmd): ...

def load_config_prefix(config): ...
