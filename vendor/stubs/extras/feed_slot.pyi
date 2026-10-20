from . import bus as bus, echelon_stepper as echelon_stepper, fm17550 as fm17550
from _typeshed import Incomplete

material_mapping: Incomplete
color_mapping: Incomplete

def is_valid_id(mapping, id): ...
def get_material_by_id(material_id): ...
def get_color_by_id(color_id): ...

class RFIDHelper:
    name: Incomplete
    printer: Incomplete
    spi: Incomplete
    mcu: Incomplete
    oid: Incomplete
    fm17550_read_card_raw: Incomplete
    fm17550_read_card: Incomplete
    gcode: Incomplete
    def __init__(self, config) -> None: ...
    def _build_config(self) -> None: ...
    def read_card(self): ...
    def cmd_READ_CARD(self, gcmd) -> None: ...

class FeedSlotHelper:
    name: Incomplete
    printer: Incomplete
    reactor: Incomplete
    gcode: Incomplete
    slot_stepper: Incomplete
    rfid_reader: Incomplete
    velocity: Incomplete
    accel: Incomplete
    min_event_systime: Incomplete
    _slot_present: Incomplete
    state: str
    info_manufacturer: int
    info_color: Incomplete
    info_material: Incomplete
    info_temp: Incomplete
    def __init__(self, config, stepper=None) -> None: ...
    def _handle_ready(self) -> None: ...
    def _note_slot_present(self, is_slot_present) -> None: ...
    def read_json_file(self, file_path) -> None: ...
    def write_json_file(self, file_path, color=None, material=None) -> None: ...
    def get_status(self, eventtime): ...

class FeedSlot:
    printer: Incomplete
    name: Incomplete
    slot_stepper: Incomplete
    buttons: Incomplete
    slot_helper: Incomplete
    chip_name: Incomplete
    mcu: Incomplete
    shift: Incomplete
    get_status: Incomplete
    def __init__(self, config) -> None: ...
    def _handle_ready(self) -> None: ...
    def _button_handler(self, eventtime, state) -> None: ...
    def _get_pin_chip_name(self, pin_desc, can_invert: bool = True, can_pullup: bool = True): ...
    def find_bit_position(self, n): ...

def load_config_prefix(config): ...
