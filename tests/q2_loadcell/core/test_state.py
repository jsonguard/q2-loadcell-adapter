from __future__ import annotations

import pytest

from q2_loadcell.core.state import FastPathState


class TestFastPathState:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.state = FastPathState()

    def test___init___WHEN_constructed_EXPECT_zero_hz_and_tare(self):
        expected = (0.0, 0.0)

        actual = (self.state.hz, self.state.tare)

        assert actual == expected
