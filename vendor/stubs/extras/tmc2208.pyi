from . import tmc as tmc, tmc2130 as tmc2130, tmc_uart as tmc_uart
from _typeshed import Incomplete

TMC_FREQUENCY: float
Registers: Incomplete
ReadRegisters: Incomplete
Fields: Incomplete
SignedFields: Incomplete
FieldFormatters: Incomplete

class TMC2208:
    fields: Incomplete
    mcu_tmc: Incomplete
    get_phase_offset: Incomplete
    get_status: Incomplete
    def __init__(self, config) -> None: ...
    def read_translate(self, reg_name, val): ...

def load_config_prefix(config): ...
