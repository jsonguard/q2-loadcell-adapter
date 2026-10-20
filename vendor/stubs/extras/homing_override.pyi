from _typeshed import Incomplete

class HomingOverride:
    printer: Incomplete
    start_pos: Incomplete
    axes: Incomplete
    template: Incomplete
    in_script: bool
    gcode: Incomplete
    prev_G28: Incomplete
    def __init__(self, config) -> None: ...
    def cmd_G28(self, gcmd) -> None: ...

def load_config(config): ...
