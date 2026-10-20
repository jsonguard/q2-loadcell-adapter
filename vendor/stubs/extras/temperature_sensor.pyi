from _typeshed import Incomplete

KELVIN_TO_CELSIUS: float

class PrinterSensorGeneric:
    printer: Incomplete
    name: Incomplete
    sensor: Incomplete
    min_temp: Incomplete
    max_temp: Incomplete
    last_temp: float
    measured_min: float
    measured_max: float
    def __init__(self, config) -> None: ...
    def temperature_callback(self, read_time, temp) -> None: ...
    def get_temp(self, eventtime): ...
    def stats(self, eventtime): ...
    def get_status(self, eventtime): ...

def load_config_prefix(config): ...
