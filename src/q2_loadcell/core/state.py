from __future__ import annotations


class FastPathState:
    """Shared run-time state between the diagnostics commands and the sampling engine."""

    __slots__ = ("hz", "tare")

    def __init__(self) -> None:
        self.hz = 0.0
        self.tare = 0.0
