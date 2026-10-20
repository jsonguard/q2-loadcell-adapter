from _typeshed import Incomplete

class SafeZHoming:
    printer: Incomplete
    z_hop: Incomplete
    z_hop_speed: Incomplete
    max_z: Incomplete
    speed: Incomplete
    move_to_previous: Incomplete
    gcode: Incomplete
    prev_G28: Incomplete
    def __init__(self, config) -> None: ...
    def cmd_G28(self, gcmd) -> None: ...

def load_config(config): ...
