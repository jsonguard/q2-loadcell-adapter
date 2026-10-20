from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from .collector import ReactorPort

_WAIT_S = 0.05
_COUNT_TIMEOUT_PER_READ_S = 0.01


@dataclass
class CaptureData:
    values: list[Any] = field(default_factory=list)
    stamps: list[float] = field(default_factory=list)
    durations: list[float] = field(default_factory=list)
    errors: int = 0
    elapsed: float = 0.0


class TimerReader:
    def __init__(self, reactor: ReactorPort, read: Optional[Callable[[], Any]], period_s: float) -> None:
        self._reactor = reactor
        self._read = read
        self._period_s = period_s
        self._timer = reactor.register_timer(self._tick, reactor.NEVER)
        self._data = CaptureData()
        self._start = 0.0
        self._deadline: Optional[float] = None
        self._remaining: Optional[int] = None
        self._done = False

    def run(
        self,
        duration_s: Optional[float] = None,
        count: Optional[int] = None,
        read: Optional[Callable[[], Any]] = None,
    ) -> CaptureData:
        if duration_s is None and count is None:
            raise ValueError("duration_s or count is required")
        if read is not None:
            self._read = read
        if self._read is None:
            raise RuntimeError("reader is not configured")
        self._data = CaptureData()
        self._done = False
        self._start = self._reactor.monotonic()
        self._deadline = self._start + duration_s if duration_s is not None else None
        self._remaining = count
        self._reactor.update_timer(self._timer, self._start)

        if duration_s is not None:
            expected_s = duration_s
        else:
            assert count is not None
            expected_s = count * max(self._period_s, _COUNT_TIMEOUT_PER_READ_S)
        hard_deadline = self._start + max(1.0, expected_s) + 2.0

        while not self._done and self._reactor.monotonic() < hard_deadline:
            self._reactor.pause(self._reactor.monotonic() + _WAIT_S)

        if not self._done:
            self._done = True
            self._reactor.update_timer(self._timer, self._reactor.NEVER)
            raise RuntimeError("capture timeout")

        self._data.elapsed = self._reactor.monotonic() - self._start
        return self._data

    def _stop(self) -> float:
        self._done = True
        return self._reactor.NEVER

    def _tick(self, eventtime: float) -> float:
        if self._done:
            return self._reactor.NEVER
        if self._deadline is not None and eventtime >= self._deadline:
            return self._stop()
        if self._remaining is not None and self._remaining <= 0:
            return self._stop()

        read = self._read
        if read is None:
            return self._stop()
        started = self._reactor.monotonic()
        try:
            self._data.values.append(read())
            self._data.stamps.append(eventtime)
        except Exception:
            self._data.errors += 1
        self._data.durations.append(self._reactor.monotonic() - started)

        if self._done:
            return self._reactor.NEVER
        if self._remaining is not None:
            self._remaining -= 1

        if self._remaining is not None and self._remaining <= 0:
            return self._stop()
        if self._deadline is not None and eventtime + self._period_s >= self._deadline:
            return self._stop()
        return eventtime + self._period_s
