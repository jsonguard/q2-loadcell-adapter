from . import bus as bus
from _typeshed import Incomplete

HTU21D_I2C_ADDR: int
HTU21D_COMMANDS: Incomplete
HTU21D_RESOLUTION_MASK: int
HTU21D_RESOLUTIONS: Incomplete
HTU21D_DEVICES: Incomplete
HTU21D_TEMP_COEFFICIENT: float
HTU21D_CRC8_POLYNOMINAL: int

class HTU21D:
    printer: Incomplete
    name: Incomplete
    reactor: Incomplete
    i2c: Incomplete
    hold_master_mode: Incomplete
    resolution: Incomplete
    report_time: Incomplete
    deviceId: Incomplete
    temp: float
    sample_timer: Incomplete
    def __init__(self, config) -> None: ...
    def handle_connect(self) -> None: ...
    min_temp: Incomplete
    max_temp: Incomplete
    def setup_minmax(self, min_temp, max_temp) -> None: ...
    _callback: Incomplete
    def setup_callback(self, cb) -> None: ...
    def get_report_time_delta(self): ...
    def _init_htu21d(self): ...
    humidity: Incomplete
    def _sample_htu21d(self, eventtime): ...
    def _chekCRC8(self, data): ...
    def get_status(self, eventtime): ...

def load_config(config) -> None: ...
