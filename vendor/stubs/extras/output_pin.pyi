from _typeshed import Incomplete

PIN_MIN_TIME: float
RESEND_HOST_TIME: Incomplete
MAX_SCHEDULE_TIME: float

class PrinterOutputPin:
    printer: Incomplete
    is_pwm: Incomplete
    mcu_pin: Incomplete
    scale: Incomplete
    last_print_time: float
    reactor: Incomplete
    resend_timer: Incomplete
    resend_interval: float
    last_value: Incomplete
    shutdown_value: Incomplete
    def __init__(self, config) -> None: ...
    def get_status(self, eventtime): ...
    def _set_pin(self, print_time, value, is_resend: bool = False) -> None: ...
    cmd_SET_PIN_help: str
    def cmd_SET_PIN(self, gcmd): ...
    def _resend_current_val(self, eventtime): ...

def load_config_prefix(config): ...
