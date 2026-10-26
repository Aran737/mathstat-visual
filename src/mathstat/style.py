"""A dark, 3Blue1Brown-inspired look for matplotlib.

Colour roles are fixed across all episodes so a viewer learns them once:
    BLUE   - the unknown truth (F, mu, E X)
    YELLOW - what we estimate from data (F_n, mu_n, sample mean)
    RED    - the error / gap between the two
    GREEN  - bounds and guarantees (Hoeffding, VC)
"""

from __future__ import annotations

import matplotlib as mpl

BG = "#0d0f14"
FG = "#e8e6e3"
GRID = "#2a2f3a"
MUTED = "#8a8f98"
BLUE = "#58c4dd"
YELLOW = "#ffd84d"
RED = "#fc6255"
GREEN = "#83c167"


def apply() -> None:
    """Set matplotlib rcParams for the series look."""
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": FG,
            "axes.titlecolor": FG,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": FG,
            "font.family": "serif",
            "font.serif": ["Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": 13,
            "axes.titlesize": 16,
            "legend.frameon": False,
            "lines.linewidth": 2.4,
        }
    )
