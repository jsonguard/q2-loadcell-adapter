from _typeshed import Incomplete

class GCodeButton:
    printer: Incomplete
    name: Incomplete
    pin: Incomplete
    last_state: int
    press_template: Incomplete
    release_template: Incomplete
    gcode: Incomplete
    def __init__(self, config) -> None: ...
    cmd_QUERY_BUTTON_help: str
    def cmd_QUERY_BUTTON(self, gcmd) -> None: ...
    def button_callback(self, eventtime, state) -> None: ...
    def get_status(self, eventtime=None): ...

def load_config_prefix(config): ...
