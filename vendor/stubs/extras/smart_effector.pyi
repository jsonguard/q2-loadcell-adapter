from . import probe as probe
from _typeshed import Incomplete

BITS_PER_SECOND: float

class ControlPinHelper:
    _mcu: Incomplete
    _pin: Incomplete
    _start_value: Incomplete
    _oid: Incomplete
    _set_cmd: Incomplete
    def __init__(self, pin_params) -> None: ...
    def _build_config(self) -> None: ...
    def write_bits(self, start_time, bit_stream): ...

class SmartEffectorProbe:
    printer: Incomplete
    gcode: Incomplete
    probe_accel: Incomplete
    recovery_time: Incomplete
    probe_wrapper: Incomplete
    get_mcu: Incomplete
    add_stepper: Incomplete
    get_steppers: Incomplete
    home_start: Incomplete
    home_wait: Incomplete
    query_endstop: Incomplete
    multi_probe_begin: Incomplete
    multi_probe_end: Incomplete
    get_position_endstop: Incomplete
    cmd_helper: Incomplete
    probe_offsets: Incomplete
    probe_session: Incomplete
    control_pin: Incomplete
    def __init__(self, config) -> None: ...
    def get_probe_params(self, gcmd=None): ...
    def get_offsets(self): ...
    def get_status(self, eventtime): ...
    def start_probe_session(self, gcmd): ...
    def probing_move(self, pos, speed): ...
    old_max_accel: Incomplete
    def probe_prepare(self, hmove) -> None: ...
    def probe_finish(self, hmove) -> None: ...
    def _send_command(self, buf) -> None: ...
    cmd_SET_SMART_EFFECTOR_help: str
    def cmd_SET_SMART_EFFECTOR(self, gcmd) -> None: ...
    cmd_RESET_SMART_EFFECTOR_help: str
    def cmd_RESET_SMART_EFFECTOR(self, gcmd) -> None: ...

def load_config(config): ...
