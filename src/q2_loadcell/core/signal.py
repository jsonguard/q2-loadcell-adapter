from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

DEFAULT_SPIKE_WIDTH: int = 5
DEFAULT_SPIKE_SIGMA: float = 6.0
_MAD_TO_SIGMA = 1.4826


@dataclass(frozen=True)
class SignalStats:
    samples: int
    duplicates: float
    stddev: float
    despiked_stddev: float
    outliers: float
    interval_median_ms: float


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _outlier_mask(
    values: Sequence[float],
    width: int = DEFAULT_SPIKE_WIDTH,
    sigma: float = DEFAULT_SPIKE_SIGMA,
) -> list[bool]:
    n = len(values)
    mask = [False] * n
    if width < 3 or n < width:
        return mask

    diffs = [values[i] - values[i - 1] for i in range(1, n)]
    diff_median = _median(diffs) if diffs else 0.0
    diff_mad = _median([abs(diff - diff_median) for diff in diffs]) if diffs else 0.0
    global_sigma = _MAD_TO_SIGMA * diff_mad / math.sqrt(2.0)

    half = width // 2
    for i, value in enumerate(values):
        window = values[max(0, i - half) : min(n, i + half + 1)]
        median = _median(window)
        local_sigma = _MAD_TO_SIGMA * _median([abs(v - median) for v in window])
        threshold = sigma * max(local_sigma, global_sigma)
        mask[i] = abs(value - median) > threshold
    return mask


def despike_filter(
    values: Sequence[float],
    width: int = DEFAULT_SPIKE_WIDTH,
    sigma: float = DEFAULT_SPIKE_SIGMA,
) -> list[float]:
    """
    Hampel filter with linear interpolation
    https://en.wikipedia.org/wiki/Hampel_test
    """
    n = len(values)
    if width < 3 or n < width:
        return list(values)

    mask = _outlier_mask(values, width, sigma)
    if not any(mask):
        return list(values)

    out = list(values)
    i = 0
    while i < n:
        if not mask[i]:
            i += 1
            continue
        start = i
        while i < n and mask[i]:
            i += 1
        end = i - 1
        prev_idx = start - 1 if start > 0 else None
        next_idx = end + 1 if end + 1 < n else None
        if prev_idx is not None and next_idx is not None:
            span = next_idx - prev_idx
            left = values[prev_idx]
            right = values[next_idx]
            for j in range(start, end + 1):
                out[j] = left + (right - left) * (j - prev_idx) / span
        elif prev_idx is not None:
            for j in range(start, end + 1):
                out[j] = values[prev_idx]
        elif next_idx is not None:
            for j in range(start, end + 1):
                out[j] = values[next_idx]
        else:
            fallback = _median(values)
            for j in range(start, end + 1):
                out[j] = fallback
    return out


def measure_rate(samples: Sequence[Sequence[float]]) -> float | None:
    if len(samples) < 2:
        return None
    span = samples[-1][0] - samples[0][0]
    if span <= 0.0:
        return None
    return (len(samples) - 1) / span


def _std(values: Sequence[float]) -> float:
    mean = sum(values) / len(values)
    return (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5


def signal_stats(
    values: Sequence[float],
    stamps: Sequence[float],
    spike_width: int = DEFAULT_SPIKE_WIDTH,
    spike_sigma: float = DEFAULT_SPIKE_SIGMA,
) -> SignalStats:
    n = len(values)
    if n < 4:
        return SignalStats(n, 0.0, 0.0, 0.0, 0.0, 0.0)

    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / n
    intervals = sorted((stamps[i] - stamps[i - 1]) * 1000.0 for i in range(1, n))
    duplicates = sum(1 for i in range(1, n) if values[i] == values[i - 1]) / (n - 1)
    outliers = sum(_outlier_mask(values, spike_width, spike_sigma)) / n
    return SignalStats(
        samples=n,
        duplicates=duplicates,
        stddev=var**0.5,
        despiked_stddev=_std(despike_filter(values, spike_width, spike_sigma)),
        outliers=outliers,
        interval_median_ms=intervals[len(intervals) // 2],
    )
