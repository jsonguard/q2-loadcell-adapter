from _typeshed import Incomplete

class ShellCommand:
    name: Incomplete
    printer: Incomplete
    gcode: Incomplete
    command: Incomplete
    timeout: Incomplete
    verbose: Incomplete
    proc_fd: Incomplete
    partial_output: str
    def __init__(self, config) -> None: ...
    def _process_output(self, eventime) -> None: ...
    cmd_RUN_SHELL_COMMAND_help: str
    def cmd_RUN_SHELL_COMMAND(self, params) -> None: ...

def load_config_prefix(config): ...
