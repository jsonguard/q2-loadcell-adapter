from _typeshed import Incomplete

respond_types: Incomplete
respond_types_no_space: Incomplete

class HostResponder:
    printer: Incomplete
    reactor: Incomplete
    default_prefix: Incomplete
    def __init__(self, config) -> None: ...
    def cmd_M118(self, gcmd) -> None: ...
    cmd_RESPOND_help: str
    def cmd_RESPOND(self, gcmd) -> None: ...

def load_config(config): ...
