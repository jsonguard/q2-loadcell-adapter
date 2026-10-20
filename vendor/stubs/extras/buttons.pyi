from _typeshed import Incomplete

QUERY_TIME: float
RETRANSMIT_COUNT: int

class MCU_buttons:
    reactor: Incomplete
    mcu: Incomplete
    pin_list: Incomplete
    callbacks: Incomplete
    invert: int
    ack_cmd: Incomplete
    ack_count: int
    def __init__(self, printer, mcu) -> None: ...
    def setup_buttons_ret(self, pins, callback): ...
    def setup_buttons(self, pins, callback) -> None: ...
    oid: Incomplete
    def build_config(self) -> None: ...
    last_button: Incomplete
    def handle_buttons_state(self, params): ...

ADC_REPORT_TIME: float
ADC_DEBOUNCE_TIME: float
ADC_SAMPLE_TIME: float
ADC_SAMPLE_COUNT: int

class MCU_ADC_buttons:
    reactor: Incomplete
    buttons: Incomplete
    last_button: Incomplete
    last_pressed: Incomplete
    last_debouncetime: int
    pullup: Incomplete
    pin: Incomplete
    min_value: float
    max_value: float
    mcu_adc: Incomplete
    def __init__(self, printer, pin, pullup) -> None: ...
    def setup_button(self, min_value, max_value, callback) -> None: ...
    def adc_callback(self, read_time, read_value) -> None: ...
    def call_button(self, button, state): ...

class BaseRotaryEncoder:
    R_START: int
    R_DIR_CW: int
    R_DIR_CCW: int
    R_DIR_MSK: int
    cw_callback: Incomplete
    ccw_callback: Incomplete
    encoder_state: Incomplete
    def __init__(self, cw_callback, ccw_callback) -> None: ...
    def encoder_callback(self, eventtime, state) -> None: ...

class FullStepRotaryEncoder(BaseRotaryEncoder):
    R_CW_FINAL: int
    R_CW_BEGIN: int
    R_CW_NEXT: int
    R_CCW_BEGIN: int
    R_CCW_FINAL: int
    R_CCW_NEXT: int
    ENCODER_STATES: Incomplete

class HalfStepRotaryEncoder(BaseRotaryEncoder):
    R_CCW_BEGIN: int
    R_CW_BEGIN: int
    R_START_M: int
    R_CW_BEGIN_M: int
    R_CCW_BEGIN_M: int
    ENCODER_STATES: Incomplete

class PrinterButtons:
    printer: Incomplete
    mcu_buttons: Incomplete
    adc_buttons: Incomplete
    def __init__(self, config) -> None: ...
    def register_adc_button(self, pin, min_val, max_val, pullup, callback) -> None: ...
    def register_adc_button_push(self, pin, min_val, max_val, pullup, callback) -> None: ...
    def register_buttons_ret(self, pins, callback): ...
    def register_buttons(self, pins, callback) -> None: ...
    def register_rotary_encoder(self, pin1, pin2, cw_callback, ccw_callback, steps_per_detent) -> None: ...
    def register_button_push(self, pin, callback) -> None: ...

def load_config(config): ...
