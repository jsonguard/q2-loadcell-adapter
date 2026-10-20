from _typeshed import Incomplete

class DelayedGcode:
    printer: Incomplete
    reactor: Incomplete
    name: Incomplete
    gcode: Incomplete
    timer_gcode: Incomplete
    duration: Incomplete
    timer_handler: Incomplete
    inside_timer: bool
    def __init__(self, config) -> None: ...
    def _handle_ready(self) -> None: ...
    def _gcode_timer_event(self, eventtime): ...
    cmd_UPDATE_DELAYED_GCODE_help: str
    repeat: Incomplete
    def cmd_UPDATE_DELAYED_GCODE(self, gcmd) -> None: ...

def load_config_prefix(config): ...
