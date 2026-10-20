from _typeshed import Incomplete

SERVO_SIGNAL_PERIOD: float
PIN_MIN_TIME: float

class PrinterServo:
    printer: Incomplete
    min_width: Incomplete
    max_width: Incomplete
    max_angle: Incomplete
    angle_to_width: Incomplete
    width_to_value: Incomplete
    last_value: float
    mcu_servo: Incomplete
    def __init__(self, config) -> None: ...
    def get_status(self, eventtime): ...
    last_value_time: Incomplete
    def _set_pwm(self, print_time, value) -> None: ...
    def _get_pwm_from_angle(self, angle): ...
    def _get_pwm_from_pulse_width(self, width): ...
    cmd_SET_SERVO_help: str
    def cmd_SET_SERVO(self, gcmd): ...

def load_config_prefix(config): ...
