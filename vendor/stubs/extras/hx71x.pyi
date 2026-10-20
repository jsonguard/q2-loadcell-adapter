from . import bulk_sensor as bulk_sensor
from _typeshed import Incomplete

UPDATE_INTERVAL: float
SAMPLE_ERROR_DESYNC: int
SAMPLE_ERROR_LONG_READ: int

class HX71xBase:
    printer: Incomplete
    name: Incomplete
    last_error_count: int
    consecutive_fails: int
    sensor_type: Incomplete
    mcu: Incomplete
    oid: Incomplete
    dout_pin: Incomplete
    sclk_pin: Incomplete
    sps: Incomplete
    gain_channel: Incomplete
    bulk_queue: Incomplete
    ffreader: Incomplete
    batch_bulk: Incomplete
    query_hx71x_cmd: Incomplete
    def __init__(self, config, sensor_type, sample_rate_options, default_sample_rate, gain_options, default_gain) -> None: ...
    def _build_config(self) -> None: ...
    def get_mcu(self): ...
    def get_samples_per_second(self): ...
    def get_range(self): ...
    def add_client(self, callback) -> None: ...
    def _convert_samples(self, samples) -> None: ...
    def _start_measurements(self) -> None: ...
    def _finish_measurements(self) -> None: ...
    def _process_batch(self, eventtime): ...

class HX711(HX71xBase):
    def __init__(self, config) -> None: ...

class HX717(HX71xBase):
    def __init__(self, config) -> None: ...

HX71X_SENSOR_TYPES: Incomplete
