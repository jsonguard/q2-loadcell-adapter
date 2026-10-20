from . import bus as bus, mcp4018 as mcp4018
from _typeshed import Incomplete

BACKGROUND_PRIORITY_CLOCK: int
PCA9632_MODE1: int
PCA9632_MODE2: int
PCA9632_PWM0: int
PCA9632_PWM1: int
PCA9632_PWM2: int
PCA9632_PWM3: int
PCA9632_LEDOUT: int
LED_PWM: int
PCA9632_LED0: int
PCA9632_LED1: int
PCA9632_LED2: int
PCA9632_LED3: int

class PCA9632:
    printer: Incomplete
    i2c: Incomplete
    color_map: Incomplete
    prev_regs: Incomplete
    led_helper: Incomplete
    def __init__(self, config) -> None: ...
    def reg_write(self, reg, val, minclock: int = 0) -> None: ...
    def handle_connect(self) -> None: ...
    def update_leds(self, led_state, print_time) -> None: ...
    def get_status(self, eventtime): ...

def load_config_prefix(config): ...
