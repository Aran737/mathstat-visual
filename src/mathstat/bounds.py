"""The inequalities used in Chapter 2.2 (proof of Theorem 2.2)."""

from __future__ import annotations

import numpy as np


def chebyshev_bound(variance: float, n: int, eps: float) -> float:
    """P(|mean of n iid r.v. - expectation| > eps) <= Var / (n * eps^2)."""
    return min(1.0, variance / (n * eps**2))


def hoeffding_bound(n: int, eps: float, a: float = 0.0, b: float = 1.0) -> float:
    """Hoeffding with a <= Z_i <= b for all i:
    P(|(1/n) sum (Z_i - E Z_i)| > eps) <= 2 exp(-2 n eps^2 / (b - a)^2)."""
    return min(1.0, 2.0 * np.exp(-2.0 * n * eps**2 / (b - a) ** 2))


def vc_bound(n: int, eps: float, shatter: float) -> float:
    """Right-hand side of Theorem 2.2 (not truncated at 1, so you can *see*
    when it is vacuous): 8 * s(A, n) * exp(-n eps^2 / 32)."""
    return 8.0 * shatter * np.exp(-n * eps**2 / 32.0)


def vc_bound_log(n: int, eps: float, log_shatter: float) -> float:
    """log of `vc_bound` - use this when s(A, n) itself overflows."""
    return np.log(8.0) + log_shatter - n * eps**2 / 32.0
