import numpy as np

from mathstat.bounds import hoeffding_bound, vc_bound, vc_bound_log


def test_hoeffding_holds_for_coin_flips():
    # Monte Carlo: the observed tail probability never exceeds the bound
    rng = np.random.default_rng(0)
    n, eps, reps = 100, 0.1, 20_000
    means = rng.integers(0, 2, size=(reps, n)).mean(axis=1)
    observed = np.mean(np.abs(means - 0.5) > eps)
    assert observed <= hoeffding_bound(n, eps, 0.0, 1.0)


def test_random_signs_step4_constant():
    # Step 4 in the notes: U_i * I_A(x_i) lies in [-1, 1], eps/4 gives exp(-n eps^2 / 32)
    n, eps = 500, 0.3
    assert np.isclose(hoeffding_bound(n, eps / 4, -1.0, 1.0), 2 * np.exp(-n * eps**2 / 32))


def test_vc_bound_vacuous_for_small_n():
    # with eps = 0.1 the bound for half-lines stays above 1 for a long time
    assert vc_bound(1000, 0.1, 1001) > 1
    assert vc_bound(100_000, 0.1, 100_001) < 1


def test_log_version_agrees():
    assert np.isclose(np.exp(vc_bound_log(5000, 0.2, np.log(5001))), vc_bound(5000, 0.2, 5001))
