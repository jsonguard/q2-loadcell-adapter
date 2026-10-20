from __future__ import annotations

from typing import Any, Callable, Mapping, Optional, Sequence


class FakeReactor:
    NEVER = 1e18

    def __init__(self, pause_step: float = 0.0, monotonic_step: float = 0.0) -> None:
        self.now = 0.0
        self.pause_step = pause_step
        self.monotonic_step = monotonic_step
        self.timer: Any = None

    def register_timer(self, callback: Any, when: float) -> int:
        self.timer = callback
        return 1

    def update_timer(self, timer_id: Any, when: float) -> None:
        pass

    def monotonic(self) -> float:
        value = self.now
        self.now += self.monotonic_step
        return value

    def pause(self, when: float) -> None:
        self.now = max(self.now, when) + self.pause_step

    def advance(self, dt: float) -> None:
        self.now += dt


class FakeTimerReactor(FakeReactor):
    def __init__(self, pause_step: float = 0.0, monotonic_step: float = 0.0) -> None:
        super().__init__(pause_step, monotonic_step)
        self._timers: dict[int, tuple[Any, float]] = {}
        self._next_timer = 1

    def register_timer(self, callback: Any, when: float) -> int:
        timer_id = self._next_timer
        self._next_timer += 1
        self._timers[timer_id] = (callback, when)
        return timer_id

    def update_timer(self, timer_id: Any, when: float) -> None:
        callback, _ = self._timers[timer_id]
        self._timers[timer_id] = (callback, when)

    def pause(self, when: float) -> None:
        target = max(self.now, when) + self.pause_step
        while True:
            due = [
                (timer_id, callback, wake)
                for timer_id, (callback, wake) in self._timers.items()
                if wake <= target and wake < self.NEVER
            ]
            if not due:
                break
            timer_id, callback, wake = min(due, key=lambda item: item[2])
            self.now = max(self.now, wake)
            next_wake = callback(wake)
            self._timers[timer_id] = (callback, next_wake)
        self.now = max(self.now, target)


class FakeConfig:
    def __init__(self, values: Optional[Mapping[str, Any]] = None, printer: Any = None) -> None:
        self.values = dict(values or {})
        self.printer = printer

    def get_printer(self) -> Any:
        return self.printer

    def get(self, option: str, default: Any = None) -> Any:
        return self.values.get(option, default)

    def getchoice(self, option: str, choices: Mapping[str, Any], default: Any = None) -> Any:
        return choices.get(str(self.values.get(option, default)), default)

    def getint(self, option: str, default: Any = None, minval: Any = None, maxval: Any = None) -> Any:
        return _clamp(int(self.values.get(option, default)), minval, maxval)

    def getfloat(self, option: str, default: Any = None, minval: Any = None, maxval: Any = None) -> Any:
        return _clamp(float(self.values.get(option, default)), minval, maxval)


def _clamp(value: Any, minval: Any, maxval: Any) -> Any:
    if minval is not None:
        value = max(value, minval)
    if maxval is not None:
        value = min(value, maxval)
    return value


class FakeSensor:
    def __init__(self, fast_values: Optional[Sequence[float]] = None, vendor_value: int = 111) -> None:
        self.fast_values = list(fast_values) if fast_values is not None else None
        self.vendor_value = vendor_value
        self.index = 0
        self.rates: list[int] = []
        self.events: list[str] = []
        self.fail_get = False
        self.fail_direct = False
        self.fail_vendor = False

    def get(self) -> Any:
        if self.fail_get:
            raise RuntimeError("no sensor")
        return self

    def oid(self) -> int:
        return 5

    def read_direct(self) -> Callable[[], float]:
        self.get()
        self.events.append("read_direct")
        if self.fast_values is None:
            raise RuntimeError("query_cs1237_end_cmd is unavailable")

        def read() -> float:
            if self.fail_direct:
                raise RuntimeError("direct read failed")
            assert self.fast_values is not None
            value = self.fast_values[self.index % len(self.fast_values)]
            self.index += 1
            return value

        return read

    def read_vendor(self) -> int:
        if self.fail_vendor:
            raise RuntimeError("vendor read failed")
        return self.vendor_value

    def type_name(self) -> str:
        return "FakeSensor"

    def set_adc_rate(self, code: int) -> Optional[str]:
        self.rates.append(code)
        self.events.append("rate:%d" % (code,))
        return None
