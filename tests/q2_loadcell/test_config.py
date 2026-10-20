from __future__ import annotations

import pytest
from fakes import FakeConfig

from q2_loadcell.config import Config


class TestConfig:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.defaults = Config(FakeConfig({}))

    def test___init___WHEN_no_options_EXPECT_tuned_defaults(self):
        expected = {
            "sweep_rate": 44,
            "restore_rate": 28,
            "median_width": 5,
            "spike_sigma": 6.0,
            "fallback_sample_hz": 250.0,
            "min_sample_hz": 100.0,
        }

        config = self.defaults
        actual = {
            "sweep_rate": config.sweep_rate,
            "restore_rate": config.restore_rate,
            "median_width": config.median_width,
            "spike_sigma": config.spike_sigma,
            "fallback_sample_hz": config.fallback_sample_hz,
            "min_sample_hz": config.min_sample_hz,
        }

        assert actual == expected

    def test___init___WHEN_options_overridden_EXPECT_parsed_values(self):
        expected = {
            "sweep_rate": 60,
            "median_width": 3,
            "spike_sigma": 4.0,
            "fallback_sample_hz": 200.0,
        }

        config = Config(
            FakeConfig(
                {
                    "sweep_rate": "60",
                    "median_width": 3,
                    "spike_sigma": 4.0,
                    "fallback_sample_hz": 200.0,
                }
            )
        )
        actual = {
            "sweep_rate": config.sweep_rate,
            "median_width": config.median_width,
            "spike_sigma": config.spike_sigma,
            "fallback_sample_hz": config.fallback_sample_hz,
        }

        assert actual == expected

    def test___init___WHEN_values_out_of_range_EXPECT_clamped(self):
        expected = {"median_width": 9, "spike_sigma": 1.0}

        config = Config(FakeConfig({"median_width": 99, "spike_sigma": 0.1}))
        actual = {"median_width": config.median_width, "spike_sigma": config.spike_sigma}

        assert actual == expected
