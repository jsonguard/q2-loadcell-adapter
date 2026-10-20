from . import adxl345 as adxl345, bulk_sensor as bulk_sensor, bus as bus
from _typeshed import Incomplete

REG_LIS2DW_WHO_AM_I_ADDR: int
REG_LIS2DW_CTRL_REG1_ADDR: int
REG_LIS2DW_CTRL_REG2_ADDR: int
REG_LIS2DW_CTRL_REG3_ADDR: int
REG_LIS2DW_CTRL_REG6_ADDR: int
REG_LIS2DW_STATUS_REG_ADDR: int
REG_LIS2DW_OUT_XL_ADDR: int
REG_LIS2DW_OUT_XH_ADDR: int
REG_LIS2DW_OUT_YL_ADDR: int
REG_LIS2DW_OUT_YH_ADDR: int
REG_LIS2DW_OUT_ZL_ADDR: int
REG_LIS2DW_OUT_ZH_ADDR: int
REG_LIS2DW_FIFO_CTRL: int
REG_LIS2DW_FIFO_SAMPLES: int
REG_MOD_READ: int
LIS2DW_DEV_ID: int
FREEFALL_ACCEL: float
SCALE: Incomplete
BATCH_UPDATES: float

class LIS2DW:
    printer: Incomplete
    axes_map: Incomplete
    data_rate: int
    spi: Incomplete
    mcu: Incomplete
    oid: Incomplete
    query_lis2dw_cmd: Incomplete
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
