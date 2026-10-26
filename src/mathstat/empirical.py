"""Empirical distribution and empirical cdf (Chapter 1.1 and 2.1).

Conventions follow the lecture: for data x_1, ..., x_n

    mu_n(B) = (1/n) * #{i : x_i in B}            (empirical distribution)
    F_n(x)  = mu_n((-inf, x])                     (empirical cdf)

Sets B are represented by *indicator functions*: a callable that takes an
array of points of shape (n, d) (or (n,) for d = 1) and returns a boolean array
of shape (n,) saying which points lie in B. This mirrors I_B(x_i) in the notes.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

Indicator = Callable[[np.ndarray], np.ndarray]


# ---------------------------------------------------------------------------
# Chapter 1.1 - the strong law of large numbers
# ---------------------------------------------------------------------------

def running_mean(x: np.ndarray) -> np.ndarray:
    """Return the path (X_1, (X_1+X_2)/2, ..., (X_1+...+X_n)/n).

    Works along the last axis, so x of shape (paths, n) gives one path per row.
    """
    x = np.asarray(x, dtype=float)
    n = np.arange(1, x.shape[-1] + 1)
    return np.cumsum(x, axis=-1) / n


# ---------------------------------------------------------------------------
# Definition 2.1 - the empirical distribution
# ---------------------------------------------------------------------------

def empirical_measure(sample: np.ndarray, indicator: Indicator) -> float:
    """mu_n(B) = (1/n) * sum_i I_B(x_i) for the set B given by `indicator`."""
    sample = np.asarray(sample, dtype=float)
    inside = np.asarray(indicator(sample), dtype=bool)
    if inside.shape != (sample.shape[0],):
        raise ValueError("indicator must return one boolean per data point")
    return float(inside.mean())


def point_masses(sample: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Support and weights of mu_n for real-valued data.

    Returns the distinct values v_1 < ... < v_k and their masses
    mu_n({v_j}) = #{i : x_i = v_j} / n. Repeated data points get a larger
    mass - each copy contributes 1/n.
    """
    values, counts = np.unique(np.asarray(sample, dtype=float), return_counts=True)
    return values, counts / counts.sum()


# ---------------------------------------------------------------------------
# Definition 2.2 - the empirical cdf
# ---------------------------------------------------------------------------

def empirical_cdf(sample: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    """Return F_n as a vectorised function of x (real-valued data only).

    F_n(x) = #{i : x_i <= x} / n. Because the interval (-inf, x] is closed on
    the right, F_n is right-continuous: at a data point it already takes the
    *upper* value of the jump.
    """
    data = np.sort(np.asarray(sample, dtype=float))
    n = data.size

    def F_n(x: np.ndarray) -> np.ndarray:
        return np.searchsorted(data, np.asarray(x, dtype=float), side="right") / n

    return F_n


def sup_distance(sample: np.ndarray, cdf: Callable[[np.ndarray], np.ndarray]) -> float:
    """Exact value of sup_x |F_n(x) - F(x)| for real data and a *continuous* cdf F.

    Between two data points F_n is constant while F is non-decreasing, so the
    supremum is approached at the data points themselves - either just at the
    jump (upper value F_n(v)) or just before it (lower value F_n(v-)).
    Checking both sides of every jump gives the exact supremum; no grid needed.
    """
    values, masses = point_masses(sample)
    upper = np.cumsum(masses)           # F_n(v)
    lower = upper - masses              # F_n(v-)  (left limit)
    F = np.asarray(cdf(values), dtype=float)
    return float(np.max(np.maximum(upper - F, F - lower)))


def argsup_distance(sample: np.ndarray, cdf: Callable[[np.ndarray], np.ndarray]):
    """Where the supremum in `sup_distance` is attained.

    Returns (x*, F_n value at the gap, F(x*)) so the gap can be drawn as a
    vertical segment from F(x*) to the relevant side of the jump.
    """
    values, masses = point_masses(sample)
    upper = np.cumsum(masses)
    lower = upper - masses
    F = np.asarray(cdf(values), dtype=float)
    gap_up, gap_low = upper - F, F - lower
    j_up, j_low = int(np.argmax(gap_up)), int(np.argmax(gap_low))
    if gap_up[j_up] >= gap_low[j_low]:
        return float(values[j_up]), float(upper[j_up]), float(F[j_up])
    return float(values[j_low]), float(lower[j_low]), float(F[j_low])
