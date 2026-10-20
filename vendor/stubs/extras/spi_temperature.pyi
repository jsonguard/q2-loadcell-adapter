from . import bus as bus
from _typeshed import Incomplete

REPORT_TIME: float
MAX_INVALID_COUNT: int

class SensorBase:
    printer: Incomplete
    chip_type: Incomplete
    _callback: Incomplete
    min_sample_value: int
    _report_clock: int
    spi: Incomplete
    mcu: Incomplete
    oid: Incomplete
    def __init__(self, config, chip_type, config_cmd=None, spi_mode: int = 1) -> None: ...
    max_sample_value: Incomplete
    def setup_minmax(self, min_temp, max_temp) -> None: ...
    def setup_callback(self, cb) -> None: ...
    def get_report_time_delta(self): ...
    def _build_config(self) -> None: ...
    def _handle_spi_response(self, params) -> None: ...
    def report_fault(self, msg) -> None: ...

MAX31856_CR0_REG: int
MAX31856_CR0_AUTOCONVERT: int
MAX31856_CR0_1SHOT: int
MAX31856_CR0_OCFAULT1: int
MAX31856_CR0_OCFAULT0: int
MAX31856_CR0_CJ: int
MAX31856_CR0_FAULT: int
MAX31856_CR0_FAULTCLR: int
MAX31856_CR0_FILT50HZ: int
MAX31856_CR0_FILT60HZ: int
MAX31856_CR1_REG: int
MAX31856_CR1_AVGSEL1: int
MAX31856_CR1_AVGSEL2: int
MAX31856_CR1_AVGSEL4: int
MAX31856_CR1_AVGSEL8: int
MAX31856_CR1_AVGSEL16: int
MAX31856_MASK_REG: int
MAX31856_MASK_COLD_JUNCTION_HIGH_FAULT: int
MAX31856_MASK_COLD_JUNCTION_LOW_FAULT: int
MAX31856_MASK_THERMOCOUPLE_HIGH_FAULT: int
MAX31856_MASK_THERMOCOUPLE_LOW_FAULT: int
MAX31856_MASK_VOLTAGE_UNDER_OVER_FAULT: int
MAX31856_MASK_THERMOCOUPLE_OPEN_FAULT: int
MAX31856_CJHF_REG: int
MAX31856_CJLF_REG: int
MAX31856_LTHFTH_REG: int
MAX31856_LTHFTL_REG: int
MAX31856_LTLFTH_REG: int
MAX31856_LTLFTL_REG: int
MAX31856_CJTO_REG: int
MAX31856_CJTH_REG: int
MAX31856_CJTL_REG: int
MAX31856_LTCBH_REG: int
MAX31856_LTCBM_REG: int
MAX31856_LTCBL_REG: int
MAX31856_SR_REG: int
MAX31856_FAULT_CJRANGE: int
MAX31856_FAULT_TCRANGE: int
MAX31856_FAULT_CJHIGH: int
MAX31856_FAULT_CJLOW: int
MAX31856_FAULT_TCHIGH: int
MAX31856_FAULT_TCLOW: int
MAX31856_FAULT_OVUV: int
MAX31856_FAULT_OPEN: int
MAX31856_SCALE: int
MAX31856_MULT: float

class MAX31856(SensorBase):
    def __init__(self, config) -> None: ...
    def handle_fault(self, adc, fault) -> None: ...
    def calc_temp(self, adc): ...
    def calc_adc(self, temp): ...
    def build_spi_init(self, config): ...

MAX31855_SCALE: int
MAX31855_MULT: float

class MAX31855(SensorBase):
    def __init__(self, config) -> None: ...
    def handle_fault(self, adc, fault) -> None: ...
    def calc_temp(self, adc): ...
    def calc_adc(self, temp): ...

MAX6675_SCALE: int
MAX6675_MULT: Incomplete

class MAX6675(SensorBase):
    def __init__(self, config) -> None: ...
    def handle_fault(self, adc, fault) -> None: ...
    def calc_temp(self, adc): ...
    def calc_adc(self, temp): ...

MAX31865_CONFIG_REG: int
MAX31865_RTDMSB_REG: int
MAX31865_RTDLSB_REG: int
MAX31865_HFAULTMSB_REG: int
MAX31865_HFAULTLSB_REG: int
MAX31865_LFAULTMSB_REG: int
MAX31865_LFAULTLSB_REG: int
MAX31865_FAULTSTAT_REG: int
MAX31865_CONFIG_BIAS: int
MAX31865_CONFIG_MODEAUTO: int
MAX31865_CONFIG_1SHOT: int
MAX31865_CONFIG_3WIRE: int
MAX31865_CONFIG_FAULTCLEAR: int
MAX31865_CONFIG_FILT50HZ: int
MAX31865_FAULT_HIGHTHRESH: int
MAX31865_FAULT_LOWTHRESH: int
MAX31865_FAULT_REFINLOW: int
MAX31865_FAULT_REFINHIGH: int
MAX31865_FAULT_RTDINLOW: int
MAX31865_FAULT_OVUV: int
MAX31865_ADC_MAX: Incomplete
CVD_A: float
CVD_B: float

class MAX31865(SensorBase):
    adc_to_resist_div_nominal: Incomplete
    config_reg: Incomplete
    def __init__(self, config) -> None: ...
    def handle_fault(self, adc, fault) -> None: ...
    def calc_temp(self, adc): ...
    def calc_adc(self, temp): ...
    def build_spi_init(self, config): ...

Sensors: Incomplete

def load_config(config) -> None: ...
