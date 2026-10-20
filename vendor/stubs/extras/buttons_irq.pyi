from _typeshed import Incomplete

class _IRQButtonMCU:
    printer: Incomplete
    reactor: Incomplete
    mcu: Incomplete
    pin_list: Incomplete
    callbacks: Incomplete
    oid: Incomplete
    ack_count: int
    state: int
    invert: int
    debounce_us: Incomplete
    def __init__(self, printer, mcu, debounce_us) -> None: ...
    def setup_buttons(self, pin_params_list, callback) -> None: ...
    ack_cmd: Incomplete
    query_cmd: Incomplete
    def _build_config(self) -> None: ...
    def query(self) -> None: ...
    def _handle_state(self, msg): ...

class MCU_irq_button:
    printer: Incomplete
    irq_buttons: Incomplete
    def __init__(self, config) -> None: ...
    def register_buttons(self, pins, callback, debounce_us, share: bool = True): ...

def load_config(config): ...
