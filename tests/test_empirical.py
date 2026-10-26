import numpy as np
from scipy.stats import norm

from mathstat.empirical import (
    argsup_distance,
    empirical_cdf,
    empirical_measure,
    point_masses,
    running_mean,
    sup_distance,
)


def test_running_mean_matches_definition():
    x = np.array([1.0, 3.0, 2.0, 6.0])
    np.testing.assert_allclose(running_mean(x), [1.0, 2.0, 2.0, 3.0])


def test_empirical_measure_is_a_probability_measure():
    rng = np.random.default_rng(0)
    x = rng.normal(size=50)
    assert empirical_measure(x, lambda p: np.ones_like(p, dtype=bool)) == 1.0
    assert empirical_measure(x, lambda p: np.zeros_like(p, dtype=bool)) == 0.0
    # additivity for disjoint sets B1 = (-inf, 0], B2 = (0, inf)
    m1 = empirical_measure(x, lambda p: p <= 0)
    m2 = empirical_measure(x, lambda p: p > 0)
    assert np.isclose(m1 + m2, 1.0)


def test_repeated_points_get_multiple_mass():
    values, masses = point_masses(np.array([0.0, 1.0, 0.0, 4.0]))
    np.testing.assert_array_equal(values, [0.0, 1.0, 4.0])
    np.testing.assert_allclose(masses, [0.5, 0.25, 0.25])


def test_empirical_cdf_is_right_continuous_step_function():
    F_n = empirical_cdf(np.array([1.0, 2.0, 2.0, 5.0]))
    assert F_n(0.999) == 0.0
    assert F_n(1.0) == 0.25          # closed interval: takes the upper value
    assert F_n(2.0) == 0.75          # jump of size 2/n at a repeated point
    assert F_n(4.999) == 0.75
    assert F_n(5.0) == 1.0


def test_empirical_cdf_equals_measure_of_halfline():
    rng = np.random.default_rng(1)
    x = rng.exponential(size=40)
    F_n = empirical_cdf(x)
    for t in [-1.0, 0.3, 1.0, 2.5]:
        assert F_n(t) == empirical_measure(x, lambda p: p <= t)


def test_sup_distance_is_exact_not_a_grid_approximation():
    rng = np.random.default_rng(2)
    x = rng.normal(size=30)
    exact = sup_distance(x, norm.cdf)
    grid = np.linspace(-5, 5, 200_001)
    approx = np.max(np.abs(empirical_cdf(x)(grid) - norm.cdf(grid)))
    assert approx <= exact + 1e-12      # a grid can only underestimate
    assert exact - approx < 1e-3        # ...and a fine grid gets close


def test_argsup_reports_the_supremum():
    rng = np.random.default_rng(3)
    x = rng.normal(size=25)
    _, fn_val, f_val = argsup_distance(x, norm.cdf)
    assert np.isclose(abs(fn_val - f_val), sup_distance(x, norm.cdf))
