from __future__ import annotations

import pytest

from q2_loadcell.core.signal import despike_filter, measure_rate, signal_stats


class TestSignal:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.step = [0.0] * 100 + [1000.0] * 100

    def test_despike_filter_WHEN_clean_step_EXPECT_values_unchanged(self):
        expected = self.step

        actual = despike_filter(self.step, 5)

        assert actual == expected

    def test_despike_filter_WHEN_linear_ramp_EXPECT_values_unchanged(self):
        expected = [float(i) for i in range(50)]

        actual = despike_filter(expected, 5)

        assert actual == expected

    def test_despike_filter_WHEN_fast_valid_transient_EXPECT_values_unchanged(self):
        values = [0.0] * 100
        values.extend((i - 99) * 5000.0 for i in range(100, 110))
        values.extend([50000.0] * 100)
        expected = values

        actual = despike_filter(values, 5)

        assert actual == expected

    def test_despike_filter_WHEN_isolated_and_paired_outliers_EXPECT_valid_values_unchanged(self):
        base = -1322000
        values: list[float] = [float(base + i) for i in range(60)]
        values[10] = -1048585.0
        values[30] = -11.0
        values[31] = -1048585.0
        expected = [float(base + i) for i in range(60)]

        actual = despike_filter(values, 5)

        assert actual == expected

    def test_despike_filter_WHEN_width_below_three_EXPECT_values_unchanged(self):
        expected = [1.0, 2.0, 3.0, 4.0]

        actual = despike_filter(expected, 1)

        assert actual == expected

    def test_despike_filter_WHEN_series_shorter_than_window_EXPECT_values_unchanged(self):
        expected = [1.0, 2.0]

        actual = despike_filter(expected, 5)

        assert actual == expected

    def test_measure_rate_WHEN_uniform_spacing_EXPECT_rate(self):
        samples = [[i * 0.005, 0.0, 0.0, 0.0] for i in range(11)]
        expected = pytest.approx(200.0)

        actual = measure_rate(samples)

        assert actual == expected

    def test_measure_rate_WHEN_single_sample_EXPECT_none(self):
        samples = [[0.0, 0.0, 0.0, 0.0]]
        expected = None

        actual = measure_rate(samples)

        assert actual is expected

    def test_measure_rate_WHEN_zero_span_EXPECT_none(self):
        samples = [[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]
        expected = None

        actual = measure_rate(samples)

        assert actual is expected

    def test_signal_stats_WHEN_constant_signal_EXPECT_all_duplicates(self):
        values = [5.0] * 20
        stamps = [i * 0.001 for i in range(20)]
        expected = {
            "samples": 20,
            "duplicates": 1.0,
            "stddev": 0.0,
            "despiked_stddev": 0.0,
            "outliers": 0.0,
            "interval_median_ms": pytest.approx(1.0),
        }

        stats = signal_stats(values, stamps)
        actual = {
            "samples": stats.samples,
            "duplicates": stats.duplicates,
            "stddev": stats.stddev,
            "despiked_stddev": stats.despiked_stddev,
            "outliers": stats.outliers,
            "interval_median_ms": stats.interval_median_ms,
        }

        assert actual == expected

    def test_signal_stats_WHEN_paired_outliers_EXPECT_despiked_sigma_and_fraction(self):
        values = [5.0] * 20
        values[5] = 1000.0
        values[6] = 1000.0
        stamps = [i * 0.001 for i in range(20)]
        expected = (pytest.approx(0.1), 0.0, True)

        stats = signal_stats(values, stamps)
        actual = (stats.outliers, stats.despiked_stddev, stats.stddev > 0.0)

        assert actual == expected

    def test_signal_stats_WHEN_series_too_short_EXPECT_zeroed_stats(self):
        expected = {"samples": 2, "stddev": 0.0, "despiked_stddev": 0.0, "outliers": 0.0}

        stats = signal_stats([1.0, 2.0], [0.0, 0.001])
        actual = {
            "samples": stats.samples,
            "stddev": stats.stddev,
            "despiked_stddev": stats.despiked_stddev,
            "outliers": stats.outliers,
        }

        assert actual == expected
