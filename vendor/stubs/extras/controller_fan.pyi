from . import fan as fan
from _typeshed import Incomplete

PIN_MIN_TIME: float

class ControllerFan:
    printer: Incomplete
    stepper_names: Incomplete
    stepper_enable: Incomplete
    heaters: Incomplete
    fan: Incomplete
    fan_speed: Incomplete
    idle_speed: Incomplete
    idle_timeout: Incomplete
    heater_names: Incomplete
    last_on: Incomplete
    last_speed: float
    def __init__(self, config) -> None: ...
    def handle_connect(self) -> None: ...
    def handle_ready(self) -> None: ...
    def get_status(self, eventtime): ...
    def callback(self, eventtime): ...

def load_config_prefix(config): ...
