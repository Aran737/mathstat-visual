import numpy as np
import pytest

from mathstat.shatter import (
    count_traces,
    is_shattered,
    shatter_coefficient_1d,
    traces_halflines,
    traces_intersection,
    traces_intervals,
    traces_quadrants,
)


@pytest.mark.parametrize("n", range(1, 9))
def test_halflines_n_plus_one(n):
    # Example 2.1 a
    assert shatter_coefficient_1d("halflines", n) == n + 1


@pytest.mark.parametrize("n", range(1, 9))
def test_intervals_closed_form(n):
    # exam question 2: contiguous blocks plus the empty set
    assert shatter_coefficient_1d("intervals", n) == n * (n + 1) // 2 + 1


@pytest.mark.parametrize("n", range(1, 9))
def test_general_bounds_from_remark(n):
    # Remark b): 1 <= s(A, n) <= 2^n
    for cls in ("halflines", "intervals"):
        assert 1 <= shatter_coefficient_1d(cls, n) <= 2**n


def test_monotone_in_n():
    # Remark c)
    for cls in ("halflines", "intervals"):
        s = [shatter_coefficient_1d(cls, n) for n in range(1, 10)]
        assert all(a <= b for a, b in zip(s, s[1:]))


def test_ties_never_help():
    # repeated points can only merge traces, so distinct points attain the max
    x = np.array([0.0, 1.0, 1.0, 2.0])
    assert count_traces(traces_halflines(x)) < shatter_coefficient_1d("halflines", 4)


def test_intervals_shatter_two_points_but_not_three():
    assert is_shattered(traces_intervals(np.array([0.0, 1.0])), 2)
    # {x1, x3} without x2 is impossible for an interval
    assert not is_shattered(traces_intervals(np.array([0.0, 1.0, 2.0])), 3)


def test_intersection_lemma_on_random_points():
    # exam question 3: s(A, n) <= s(A1, n) * s(A2, n), checked trace-wise:
    # on every fixed configuration, #traces(A1 ∩ A2) <= #traces(A1) * #traces(A2)
    rng = np.random.default_rng(0)
    for _ in range(50):
        n = int(rng.integers(1, 8))
        x = rng.normal(size=n)
        t1 = traces_halflines(x)
        t2 = traces_halflines(-x)            # sets of the form [-t, inf)
        both = traces_intersection(t1, t2)   # these are exactly intervals
        assert count_traces(both) <= count_traces(t1) * count_traces(t2)
        assert both == traces_intervals(x)


@pytest.mark.parametrize("d", [1, 2, 3])
def test_quadrants_bound(d):
    # Example 2.1 b: s(A, n) <= (n + 1)^d
    rng = np.random.default_rng(d)
    for n in range(1, 7):
        x = rng.normal(size=(n, d))
        assert count_traces(traces_quadrants(x)) <= (n + 1) ** d
