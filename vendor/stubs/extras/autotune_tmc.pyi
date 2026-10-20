from . import tmc as tmc
from _typeshed import Incomplete
from enum import Enum

TUNING_GOAL: str
EXTRA_HYSTERESIS: int
TBL: int
TOFF: int
SGT: int
SG4_THRS: int
VOLTAGE: float
OVERVOLTAGE_VTH: Incomplete
COOLSTEP_THRS_FACTOR: float
FULLSTEP_THRS_FACTOR: float
MULTISTEP_FILT: bool
PWM_AUTOSCALE: bool
PWM_AUTOGRAD: bool
PWM_REG: int
PWM_LIM: int
PWM_FREQ_TARGET: float
TPFD: int
FAST_STANDSTILL: bool
SMALL_HYSTERESIS: bool
SEMIN: int
SEMAX: int
SEUP: int
SEDN: int
SEIMIN: int
SFILT: int
IHOLDDELAY: int
IRUNDELAY: int
VHIGHFS: bool
VHIGHCHM: bool
TRINAMIC_DRIVERS: Incomplete
AUTO_PERFORMANCE_MOTORS: Incomplete

class TuningGoal(str, Enum):
    AUTO: str
    AUTOSWITCH: str
    SILENT: str
    PERFORMANCE: str

class AutotuneTMC:
    printer: Incomplete
    name: Incomplete
    tmc_section: Incomplete
    driver_name: Incomplete
    _set_driver_velocity_field: Incomplete
    motor: Incomplete
    motor_name: Incomplete
    tuning_goal: Incomplete
    auto_silent: bool
    tmc_object: Incomplete
    tmc_cmdhelper: Incomplete
    tmc_init_registers: Incomplete
    run_current: float
    fclk: Incomplete
    motor_object: Incomplete
    extra_hysteresis: Incomplete
    tbl: Incomplete
    toff: Incomplete
    tpfd: Incomplete
    sgt: Incomplete
    sg4_thrs: Incomplete
    voltage: Incomplete
    overvoltage_vth: Incomplete
    pwm_freq_target: Incomplete
    def __init__(self, config) -> None: ...
    def handle_connect(self) -> None: ...
    def handle_ready(self) -> None: ...
    cmd_AUTOTUNE_TMC_help: str
    def cmd_AUTOTUNE_TMC(self, gcmd) -> None: ...
    def tune_driver(self, print_time=None) -> None: ...
    def _set_driver_field(self, field, arg) -> None: ...
    def _set_driver_velocity_field_new(self, field, velocity) -> None: ...
    def _set_driver_velocity_field_old(self, field, velocity) -> None: ...
    def _set_pwmfreq(self) -> None: ...
    def _set_hysteresis(self, run_current) -> None: ...
    def _set_sg4thrs(self) -> None: ...
    def _pwmthrs(self, vmaxpwm, coolthrs): ...
    def _setup_pwm(self, tgoal, pwmthrs) -> None: ...
    def _setup_spreadcycle(self) -> None: ...
    def _setup_coolstep(self, coolthrs) -> None: ...
    def _setup_highspeed(self, vhigh) -> None: ...

def load_config_prefix(config): ...
