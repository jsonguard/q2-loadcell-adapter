from . import bus as bus
from _typeshed import Incomplete

WiperRegisters: Incomplete

class mcp4451:
    i2c: Incomplete
    def __init__(self, config) -> None: ...
    def set_register(self, reg, value) -> None: ...

def load_config_prefix(config): ...
