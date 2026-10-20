from __future__ import annotations

from typing import Any, Mapping, Protocol

from .hardware.constants import ADC_RATE_HZ

_RATE_CHOICES: dict[str, int] = {str(code): code for code in ADC_RATE_HZ}


class ConfigPort(Protocol):
    def get_printer(self) -> Any: ...
    def getchoice(self, option: str, choices: Mapping[str, Any], default: Any = ...) -> Any: ...
    def getint(self, option: str, default: Any = ..., minval: Any = None, maxval: Any = None) -> int: ...
    def getfloat(self, option: str, default: Any = ..., minval: Any = None, maxval: Any = None) -> float: ...


class Config:
    def __init__(self, config: ConfigPort) -> None:
        # Sampling
        self.sweep_rate: int = config.getchoice("sweep_rate", _RATE_CHOICES, "44")
        self.restore_rate: int = config.getchoice("restore_rate", _RATE_CHOICES, "28")
        self.median_width: int = config.getint("median_width", 5, minval=1, maxval=9)
        self.spike_sigma: float = config.getfloat("spike_sigma", 6.0, minval=1.0)
        # Timing
        self.fallback_sample_hz: float = config.getfloat("fallback_sample_hz", 250.0, minval=1.0)
        self.min_sample_hz: float = config.getfloat("min_sample_hz", 100.0, minval=1.0)
