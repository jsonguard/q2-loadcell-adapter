from _typeshed import Incomplete

GCC_CMD: str
COMPILE_ARGS: str
SSE_FLAGS: str
SOURCE_FILES: Incomplete
DEST_LIB: str
OTHER_FILES: Incomplete
defs_stepcompress: str
defs_itersolve: str
defs_trapq: str
defs_kin_cartesian: str
defs_kin_corexy: str
defs_kin_corexz: str
defs_kin_delta: str
defs_kin_deltesian: str
defs_kin_polar: str
defs_kin_rotary_delta: str
defs_kin_winch: str
defs_kin_extruder: str
defs_kin_shaper: str
defs_kin_idex: str
defs_serialqueue: str
defs_trdispatch: str
defs_pyhelper: str
defs_std: str
defs_all: Incomplete

def get_abs_files(srcdir, filelist): ...
def get_mtimes(filelist): ...
def check_build_code(sources, target): ...
def check_gcc_option(option): ...
def do_build_code(cmd) -> None: ...

FFI_main: Incomplete
FFI_lib: Incomplete
pyhelper_logging_callback: Incomplete

def logging_callback(msg) -> None: ...
def get_ffi(): ...

HC_COMPILE_CMD: str
HC_SOURCE_FILES: Incomplete
HC_SOURCE_DIR: str
HC_TARGET: str
HC_CMD: str

def run_hub_ctrl(enable_power) -> None: ...
