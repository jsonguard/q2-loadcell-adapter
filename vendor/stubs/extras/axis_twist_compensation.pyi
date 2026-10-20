from . import bed_mesh as bed_mesh, manual_probe as manual_probe, probe as probe
from _typeshed import Incomplete

DEFAULT_SAMPLE_COUNT: int
DEFAULT_SPEED: float
DEFAULT_HORIZONTAL_MOVE_Z: float

class AxisTwistCompensation:
    printer: Incomplete
    gcode: Incomplete
    horizontal_move_z: Incomplete
    speed: Incomplete
    calibrate_start_x: Incomplete
    calibrate_end_x: Incomplete
    calibrate_y: Incomplete
    z_compensations: Incomplete
    compensation_start_x: Incomplete
    compensation_end_x: Incomplete
    m: Incomplete
    b: Incomplete
    calibrater: Incomplete
    def __init__(self, config) -> None: ...
    def _update_z_compensation_value(self, pos) -> None: ...
    def clear_compensations(self) -> None: ...

class Calibrater:
    compensation: Incomplete
    printer: Incomplete
    gcode: Incomplete
    probe: Incomplete
    speed: Incomplete
    horizontal_move_z: Incomplete
    start_point: Incomplete
    end_point: Incomplete
    results: Incomplete
    current_point_index: Incomplete
    gcmd: Incomplete
    configname: Incomplete
    def __init__(self, compensation, config) -> None: ...
    lift_speed: Incomplete
    def _handle_connect(self) -> None: ...
    def _register_gcode_handlers(self) -> None: ...
    cmd_AXIS_TWIST_COMPENSATION_CALIBRATE_help: str
    def cmd_AXIS_TWIST_COMPENSATION_CALIBRATE(self, gcmd) -> None: ...
    def _calculate_nozzle_points(self, sample_count, interval_dist): ...
    def _calculate_probe_points(self, nozzle_points, probe_x_offset, probe_y_offset): ...
    def _move_helper(self, target_coordinates, override_speed=None) -> None: ...
    current_measured_z: Incomplete
    def _calibration(self, probe_points, nozzle_points, interval) -> None: ...
    def _manual_probe_callback_factory(self, probe_points, nozzle_points, interval): ...
    def _finalize_calibration(self) -> None: ...

def load_config(config): ...
