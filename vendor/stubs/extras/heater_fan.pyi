from . import fan as fan
from _typeshed import Incomplete

PIN_MIN_TIME: float

class PrinterHeaterFan:
    printer: Incomplete
    heater_names: Incomplete
    heater_temp: Incomplete
    heaters: Incomplete
    fan: Incomplete
    fan_speed: Incomplete
    last_speed: float
    def __init__(self, config) -> None: ...
    def handle_ready(self) -> None: ...
    def get_status(self, eventtime): ...
    def callback(self, eventtime): ...

def load_config_prefix(config): ...
