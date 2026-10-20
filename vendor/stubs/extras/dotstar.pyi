from . import bus as bus
from _typeshed import Incomplete

BACKGROUND_PRIORITY_CLOCK: int

class PrinterDotstar:
    printer: Incomplete
    spi: Incomplete
    chain_count: Incomplete
    led_helper: Incomplete
    prev_data: Incomplete
    def __init__(self, config) -> None: ...
    def handle_connect(self) -> None: ...
    def update_leds(self, led_state, print_time) -> None: ...
    def get_status(self, eventtime): ...

def load_config_prefix(config): ...
