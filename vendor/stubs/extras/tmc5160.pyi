from . import bus as bus, tmc as tmc, tmc2130 as tmc2130
from _typeshed import Incomplete

TMC_FREQUENCY: float
Registers: Incomplete
ReadRegisters: Incomplete
Fields: Incomplete
SignedFields: Incomplete
FieldFormatters: Incomplete
VREF: float
MAX_CURRENT: float

class TMC5160CurrentHelper:
    printer: Incomplete
    name: Incomplete
    mcu_tmc: Incomplete
    fields: Incomplete
    req_hold_current: Incomplete
    sense_resistor: Incomplete
    def __init__(self, config, mcu_tmc) -> None: ...
    def _calc_globalscaler(self, current): ...
    def _calc_current_bits(self, current, globalscaler): ...
    def _calc_current(self, run_current, hold_current): ...
    def _calc_current_from_field(self, field_name): ...
    def get_current(self): ...
    def set_current(self, run_current, hold_current, print_time) -> None: ...

class TMC5160:
    fields: Incomplete
    mcu_tmc: Incomplete
    get_phase_offset: Incomplete
    get_status: Incomplete
    def __init__(self, config) -> None: ...

def load_config_prefix(config): ...
