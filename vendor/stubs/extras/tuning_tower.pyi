from _typeshed import Incomplete

CANCEL_Z_DELTA: float

class TuningTower:
    printer: Incomplete
    normal_transform: Incomplete
    last_position: Incomplete
    last_z: float
    last_command_value: Incomplete
    command_fmt: str
    gcode_move: Incomplete
    gcode: Incomplete
    def __init__(self, config) -> None: ...
    cmd_TUNING_TOWER_help: str
    start: Incomplete
    factor: Incomplete
    band: Incomplete
    step_delta: Incomplete
    step_height: Incomplete
    skip: Incomplete
    def cmd_TUNING_TOWER(self, gcmd) -> None: ...
    def get_position(self): ...
    def calc_value(self, z): ...
    def move(self, newpos, speed) -> None: ...
    def end_test(self) -> None: ...
    def is_active(self): ...

def load_config(config): ...
