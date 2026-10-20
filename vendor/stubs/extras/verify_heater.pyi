from _typeshed import Incomplete

HINT_THERMAL: str

class HeaterCheck:
    printer: Incomplete
    heater_name: Incomplete
    heater: Incomplete
    hysteresis: Incomplete
    max_error: Incomplete
    heating_gain: Incomplete
    position_z: Incomplete
    check_gain_time: Incomplete
    approaching_target: bool
    last_target: float
    goal_systime: Incomplete
    check_timer: Incomplete
    is_box_heater: Incomplete
    def __init__(self, config) -> None: ...
    def handle_connect(self) -> None: ...
    def handle_shutdown(self) -> None: ...
    error: float
    goal_temp: Incomplete
    starting_approach: bool
    def check_event(self, eventtime): ...
    def heater_fault(self): ...
    def box_heater_fault(self) -> None: ...

def load_config_prefix(config): ...
