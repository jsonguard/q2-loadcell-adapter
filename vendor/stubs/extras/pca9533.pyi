from . import bus as bus
from _typeshed import Incomplete

BACKGROUND_PRIORITY_CLOCK: int
PCA9533_PWM0: int
PCA9533_PWM1: int
PCA9533_PLS0: int

class PCA9533:
    printer: Incomplete
    i2c: Incomplete
    led_helper: Incomplete
    def __init__(self, config) -> None: ...
    def update_leds(self, led_state, print_time) -> None: ...
    def get_status(self, eventtime): ...

def load_config_prefix(config): ...
