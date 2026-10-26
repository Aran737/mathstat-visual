"""Shatter coefficients (Definition 2.3, Example 2.1).

    s(A, n) = max over x_1..x_n of #{ A ∩ {x_1, ..., x_n} : A in A }

A "trace" A ∩ {x_1, ..., x_n} is stored as a frozenset of point *indices*.

Honest caveat: the maximum over *all* point configurations in R^d cannot be
searched by brute force. Two ways around it are used here:

* For the 1-d classes below the traces only depend on the *order* of the
  points, and ties can only merge traces. So n distinct points already attain
  the maximum, and `shatter_coefficient_1d` is exact. (Proving this ordering
  argument is a nice exercise in itself.)
* For other classes, `count_traces` counts the traces on *given* points. That
  is a lower bound for s(A, n) and is used to test inequalities such as
  s(A, n) <= s(A1, n) * s(A2, n) on random configurations.
"""

from __future__ import annotations

from itertools import combinations_with_replacement, product
from typing import Iterable

import numpy as np

Trace = frozenset


def _thresholds_1d(x: np.ndarray) -> np.ndarray:
    """Cut points that realise every distinct trace of half-lines/intervals:
    one point left of everything, every data point, and the midpoints."""
    v = np.unique(x)
    mids = (v[:-1] + v[1:]) / 2 if v.size > 1 else np.array([])
    return np.concatenate([[v[0] - 1.0], v, mids, [v[-1] + 1.0]])


# ---------------------------------------------------------------------------
# Traces of concrete classes
# ---------------------------------------------------------------------------

def traces_halflines(x: np.ndarray) -> set[Trace]:
    """Traces of A = {(-inf, t] : t in R} on the real points x."""
    x = np.asarray(x, dtype=float)
    return {frozenset(np.flatnonzero(x <= t).tolist()) for t in _thresholds_1d(x)}


def traces_intervals(x: np.ndarray) -> set[Trace]:
    """Traces of A = {[a, b] : a <= b} on the real points x (empty set included,
    since an interval can always avoid all points)."""
    x = np.asarray(x, dtype=float)
    cuts = np.sort(_thresholds_1d(x))
    traces = {frozenset()}
    for a, b in combinations_with_replacement(cuts, 2):
        traces.add(frozenset(np.flatnonzero((x >= a) & (x <= b)).tolist()))
    return traces


def traces_quadrants(x: np.ndarray) -> set[Trace]:
    """Traces of A = {(-inf, z] : z in R^d} on points x of shape (n, d)
    (Example 2.1 b - lower-left orthants)."""
    x = np.asarray(x, dtype=float)
    cuts = [_thresholds_1d(x[:, k]) for k in range(x.shape[1])]
    return {
        frozenset(np.flatnonzero(np.all(x <= np.array(z), axis=1)).tolist())
        for z in product(*cuts)
    }


def traces_intersection(t1: Iterable[Trace], t2: Iterable[Trace]) -> set[Trace]:
    """Traces of {A1 ∩ A2 : A1 in A1, A2 in A2}, built from the traces of the
    two classes on the same points - exactly the step used in the proof:
    (A1 ∩ A2) ∩ {x} = (A1 ∩ {x}) ∩ (A2 ∩ {x})."""
    t2 = list(t2)
    return {a & b for a in t1 for b in t2}


def count_traces(traces: Iterable[Trace]) -> int:
    return len(set(traces))


# ---------------------------------------------------------------------------
# Exact shatter coefficients in d = 1
# ---------------------------------------------------------------------------

_CLASSES_1D = {"halflines": traces_halflines, "intervals": traces_intervals}


def shatter_coefficient_1d(cls: str, n: int) -> int:
    """s(A, n) for A = 'halflines' or 'intervals', computed by brute force on
    n distinct points (which attain the maximum, see module docstring)."""
    if cls not in _CLASSES_1D:
        raise ValueError(f"unknown class {cls!r}, choose from {sorted(_CLASSES_1D)}")
    return count_traces(_CLASSES_1D[cls](np.arange(n, dtype=float)))


def is_shattered(traces: Iterable[Trace], n: int) -> bool:
    """True if all 2^n subsets of the n points appear as traces."""
    return count_traces(traces) == 2 ** n
