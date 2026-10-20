from __future__ import annotations

import pytest
from fakes import FakeReactor, FakeTimerReactor

from q2_loadcell.core.capture import TimerReader


class TestTimerReader:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reactor = FakeTimerReactor()
        self.reads = 0

    def read(self) -> int:
        self.reads += 1
        return self.reads

    def test_run_WHEN_duration_EXPECT_timer_driven_samples(self):
        reader = TimerReader(self.reactor, self.read, period_s=0.01)
        expected = [1, 2, 3, 4, 5]

        data = reader.run(duration_s=0.05)
        actual = data.values

        assert actual == expected
        assert len(data.stamps) == len(actual)
        assert len(data.durations) == len(actual)
        assert data.errors == 0
        assert data.elapsed > 0.0

    def test_run_WHEN_count_EXPECT_exact_samples(self):
        reader = TimerReader(self.reactor, self.read, period_s=0.01)
        expected = [1, 2, 3, 4, 5]

        data = reader.run(count=5)
        actual = data.values

        assert actual == expected

    def test_run_WHEN_read_override_EXPECT_override_used(self):
        reader = TimerReader(self.reactor, self.read, period_s=0.01)
        expected = [99, 99]

        data = reader.run(count=2, read=lambda: 99)
        actual = data.values

        assert actual == expected

    def test_run_WHEN_reads_fail_EXPECT_errors_without_abort(self):
        expected_values = []
        expected_errors = 3
        expected_durations = 3

        def read() -> int:
            raise RuntimeError("read failed")

        reader = TimerReader(self.reactor, read, period_s=0.01)
        data = reader.run(count=3)
        actual = (data.values, data.errors, len(data.durations))

        assert actual == (expected_values, expected_errors, expected_durations)

    def test_run_WHEN_timer_does_not_fire_EXPECT_timeout(self):
        expected = "capture timeout"
        reader = TimerReader(FakeReactor(), self.read, period_s=0.01)

        with pytest.raises(RuntimeError) as excinfo:
            reader.run(duration_s=0.05)
        actual = str(excinfo.value)

        assert actual == expected
