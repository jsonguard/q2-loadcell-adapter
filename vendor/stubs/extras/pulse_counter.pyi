from _typeshed import Incomplete

class MCU_counter:
    _mcu: Incomplete
    _oid: Incomplete
    _pin: Incomplete
    _pullup: Incomplete
    _poll_time: Incomplete
    _poll_ticks: int
    _sample_time: Incomplete
    _callback: Incomplete
    _last_count: int
    def __init__(self, printer, pin, sample_time, poll_time) -> None: ...
    def build_config(self) -> None: ...
    def setup_callback(self, cb) -> None: ...
    def _handle_counter_state(self, params) -> None: ...

class FrequencyCounter:
    _callback: Incomplete
    _last_time: Incomplete
    _freq: float
    _counter: Incomplete
    def __init__(self, printer, pin, sample_time, poll_time) -> None: ...
    _last_count: Incomplete
    def _counter_callback(self, time, count, count_time) -> None: ...
    def get_frequency(self): ...
