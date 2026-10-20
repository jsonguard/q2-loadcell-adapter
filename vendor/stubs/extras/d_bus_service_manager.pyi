from _typeshed import Incomplete
from dbus_fast.message import Message

class DBus:
    MethodExecute: str
    class Signal:
        Object: str
        Interface: str
    class Klipper:
        Service: str
        Object: str
        Interface: str
    class Moonraker:
        Service: str
        Object: str
        Interface: str
    class QidiClient:
        Service: str
        Object: str
        Interface: str

class DBusConnection:
    reactor: Incomplete
    bus_address: Incomplete
    on_message_callback: Incomplete
    sock: Incomplete
    fd_handle: Incomplete
    unmarshaller: Incomplete
    send_buffer: bytes
    is_blocking: bool
    _serial: int
    def __init__(self, reactor, bus_address, on_message_callback) -> None: ...
    def _connect(self) -> None: ...
    def send_message(self, message: Message): ...
    def _do_send(self, eventtime=None): ...
    def process_received(self, eventtime): ...
    def close(self) -> None: ...

class DBusServiceManager:
    printer: Incomplete
    reactor: Incomplete
    method_handlers: Incomplete
    pending_requests: Incomplete
    signal_handlers: Incomplete
    conn: Incomplete
    def __init__(self, config) -> None: ...
    def _init_dbus(self): ...
    def register_local_method(self, method_name, handler) -> None: ...
    def register_signal_cb(self, event, callback, sender: str = '*') -> None: ...
    def call_remote(self, target, method, params=None, callback=None) -> None: ...
    def call_signal(self, signal, params) -> None: ...
    def _on_message_received(self, msg: Message): ...
    def call_moonraker(self, method, params=None, callback=None) -> None: ...
    def call_qidi_client(self, method, params=None, callback=None) -> None: ...

def load_config(config): ...
