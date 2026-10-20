from . import bulk_sensor as bulk_sensor, bus as bus
from _typeshed import Incomplete

MIN_MSG_TIME: float
BATCH_UPDATES: float
LDC1612_ADDR: int
LDC1612_FREQ: int
SETTLETIME: float
DRIVECUR: int
DEGLITCH: int
LDC1612_MANUF_ID: int
LDC1612_DEV_ID: int
REG_RCOUNT0: int
REG_OFFSET0: int
REG_SETTLECOUNT0: int
REG_CLOCK_DIVIDERS0: int
REG_ERROR_CONFIG: int
REG_CONFIG: int
REG_MUX_CONFIG: int
REG_DRIVE_CURRENT0: int
REG_MANUFACTURER_ID: int
REG_DEVICE_ID: int

class DriveCurrentCalibrate:
    printer: Incomplete
    sensor: Incomplete
    drive_cur: Incomplete
    name: Incomplete
    def __init__(self, config, sensor) -> None: ...
    def get_drive_current(self): ...
    cmd_LDC_CALIBRATE_help: str
    def cmd_LDC_CALIBRATE(self, gcmd): ...

class LDC1612:
    printer: Incomplete
    calibration: Incomplete
    dccal: Incomplete
    data_rate: int
    i2c: Incomplete
    mcu: Incomplete
    oid: Incomplete
    query_ldc1612_cmd: Incomplete
    ldc1612_setup_home_cmd: Incomplete
    ffreader: Incomplete
    last_error_count: int
    batch_bulk: Incomplete
    name: Incomplete
    def __init__(self, config, calibration=None) -> None: ...
    query_ldc1612_home_state_cmd: Incomplete
    def _build_config(self) -> None: ...
    def get_mcu(self): ...
    def read_reg(self, reg): ...
    def set_reg(self, reg, val, minclock: int = 0) -> None: ...
    def add_client(self, cb) -> None: ...
    def setup_home(self, print_time, trigger_freq, trsync_oid, hit_reason, err_reason) -> None: ...
    def clear_home(self): ...
    def _convert_samples(self, samples) -> None: ...
    def _start_measurements(self) -> None: ...
    def _finish_measurements(self) -> None: ...
    def _process_batch(self, eventtime): ...
