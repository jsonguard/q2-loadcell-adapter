from . import bulk_sensor as bulk_sensor, bus as bus
from _typeshed import Incomplete
from typing import NamedTuple

REG_DEVID: int
REG_BW_RATE: int
REG_POWER_CTL: int
REG_DATA_FORMAT: int
REG_FIFO_CTL: int
REG_MOD_READ: int
REG_MOD_MULTI: int
QUERY_RATES: Incomplete
ADXL345_DEV_ID: int
SET_FIFO_CTL: int
FREEFALL_ACCEL: Incomplete
SCALE_XY: Incomplete
SCALE_Z: Incomplete

class Accel_Measurement(NamedTuple):
    time: Incomplete
    accel_x: Incomplete
    accel_y: Incomplete
    accel_z: Incomplete

class AccelQueryHelper:
    printer: Incomplete
    is_finished: bool
    request_start_time: Incomplete
    msgs: Incomplete
    samples: Incomplete
    def __init__(self, printer) -> None: ...
    request_end_time: Incomplete
    def finish_measurements(self) -> None: ...
    def handle_batch(self, msg): ...
    def has_valid_samples(self): ...
    def get_samples(self): ...
    def write_to_file(self, filename) -> None: ...

class AccelCommandHelper:
    printer: Incomplete
    chip: Incomplete
    bg_client: Incomplete
    base_name: Incomplete
    name: Incomplete
    def __init__(self, config, chip) -> None: ...
    def register_commands(self, name) -> None: ...
    cmd_ACCELEROMETER_MEASURE_help: str
    def cmd_ACCELEROMETER_MEASURE(self, gcmd) -> None: ...
    cmd_ACCELEROMETER_QUERY_help: str
    def cmd_ACCELEROMETER_QUERY(self, gcmd) -> None: ...
    cmd_ACCELEROMETER_DEBUG_READ_help: str
    def cmd_ACCELEROMETER_DEBUG_READ(self, gcmd): ...
    cmd_ACCELEROMETER_DEBUG_WRITE_help: str
    def cmd_ACCELEROMETER_DEBUG_WRITE(self, gcmd): ...

def read_axes_map(config, scale_x, scale_y, scale_z): ...

BATCH_UPDATES: float

class ADXL345:
    printer: Incomplete
    axes_map: Incomplete
    data_rate: Incomplete
    spi: Incomplete
    mcu: Incomplete
    oid: Incomplete
    query_adxl345_cmd: Incomplete
    ffreader: Incomplete
    last_error_count: int
    batch_bulk: Incomplete
    name: Incomplete
    def __init__(self, config) -> None: ...
    def _build_config(self) -> None: ...
    def read_reg(self, reg): ...
    def set_reg(self, reg, val, minclock: int = 0) -> None: ...
    def start_internal_client(self): ...
    def _convert_samples(self, samples) -> None: ...
    def _start_measurements(self) -> None: ...
    def _finish_measurements(self) -> None: ...
    def _process_batch(self, eventtime): ...

def load_config(config): ...
def load_config_prefix(config): ...
