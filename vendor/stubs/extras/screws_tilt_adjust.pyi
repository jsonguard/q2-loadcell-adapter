from . import probe as probe
from _typeshed import Incomplete

class ScrewsTiltAdjust:
    config: Incomplete
    printer: Incomplete
    screws: Incomplete
    results: Incomplete
    max_diff: Incomplete
    max_diff_error: bool
    threads: Incomplete
    thread: Incomplete
    probe_helper: Incomplete
    gcode: Incomplete
    def __init__(self, config) -> None: ...
    cmd_SCREWS_TILT_CALCULATE_help: str
    direction: Incomplete
    def cmd_SCREWS_TILT_CALCULATE(self, gcmd) -> None: ...
    def get_status(self, eventtime): ...
    def probe_finalize(self, offsets, positions): ...

def load_config(config): ...
