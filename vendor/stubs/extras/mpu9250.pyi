from . import adxl345 as adxl345, bulk_sensor as bulk_sensor, bus as bus
from _typeshed import Incomplete

MPU9250_ADDR: int
MPU_DEV_IDS: Incomplete
REG_DEVID: int
REG_FIFO_EN: int
REG_SMPLRT_DIV: int
REG_CONFIG: int
REG_ACCEL_CONFIG: int
REG_ACCEL_CONFIG2: int
REG_USER_CTRL: int
REG_PWR_MGMT_1: int
REG_PWR_MGMT_2: int
REG_INT_STATUS: int
SAMPLE_RATE_DIVS: Incomplete
SET_CONFIG: int
SET_ACCEL_CONFIG: int
SET_ACCEL_CONFIG2: int
SET_PWR_MGMT_1_WAKE: int
SET_PWR_MGMT_1_SLEEP: int
SET_PWR_MGMT_2_ACCEL_ON: int
SET_PWR_MGMT_2_OFF: int
SET_USER_FIFO_RESET: int
SET_USER_FIFO_EN: int
SET_ENABLE_FIFO: int
SET_DISABLE_FIFO: int
FREEFALL_ACCEL: Incomplete
SCALE: Incomplete
FIFO_SIZE: int
BATCH_UPDATES: float

class MPU9250:
    printer: Incomplete
    axes_map: Incomplete
    data_rate: Incomplete
    i2c: Incomplete
    mcu: Incomplete
    oid: Incomplete
    query_mpu9250_cmd: Incomplete
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
