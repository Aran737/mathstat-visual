"""Episode 03 - Glivenko-Cantelli (Theorem 2.1).

    sup_x |F_n(x) - F(x)|  ->  0   almost surely.

What the animation shows
------------------------
Left:  the true cdf F (blue) and the empirical cdf F_n (yellow) of ONE sample
       X_1, X_2, ... that keeps growing. The red segment marks where the
       distance between the two curves is largest.
Right: that largest distance D_n against n (log-log). The yellow curve is the
       sample on the left; the grey curves are 40 other samples (other omegas).

Prediction to write down before rendering
-----------------------------------------
* How does D_n behave for n = 1? (Hint: F_n jumps from 0 to 1 in one step.)
* Does D_n decrease monotonically?
* Roughly how fast does it shrink? Halving the error costs how many more points?

What the simulation can NOT show
--------------------------------
We only ever see finitely many n and finitely many omegas. "Almost surely"
is a statement about every omega outside a null set and about n -> infinity.
That needs the proof: Theorem 2.2 + Corollary 2.3 + Borel-Cantelli.
The 1/sqrt(n) rate seen on the right is an observation, not something
Chapter 2 proves.

Run:  python episodes/ep03_glivenko_cantelli.py            (mp4 + gif in media/)
      python episodes/ep03_glivenko_cantelli.py --preview  (a few PNG frames)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation, PillowWriter
from scipy.stats import norm

from mathstat import style
from mathstat.empirical import argsup_distance, sup_distance

N_MAX = 2000
N_OTHER = 40
SEED = 11          # a typical sample; try others and compare!
SEED_OTHERS = 1000
X_RANGE = (-3.8, 3.8)

INTRO, GROW, OUTRO = 2.5, 14.0, 4.0  # seconds


def sup_path(sample: np.ndarray, ns: np.ndarray) -> np.ndarray:
    return np.array([sup_distance(sample[:n], norm.cdf) for n in ns])


def build(fps: int):
    style.apply()
    sample = np.random.default_rng(SEED).normal(size=N_MAX)
    others = np.random.default_rng(SEED_OTHERS).normal(size=(N_OTHER, N_MAX))

    n_grow = int(GROW * fps)
    ns = np.unique(np.round(np.geomspace(1, N_MAX, n_grow)).astype(int))
    # one frame per n, stretched to fill the GROW phase
    frame_ns = ns[np.linspace(0, ns.size - 1, n_grow).round().astype(int)]
    d_main = sup_path(sample, ns)
    d_other = np.array([sup_path(o, ns) for o in others])

    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1], left=0.06, right=0.97,
                          top=0.80, bottom=0.155, wspace=0.22)
    ax = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    title = fig.text(0.5, 0.92, "Glivenko–Cantelli", ha="center", fontsize=26)
    subtitle = fig.text(0.5, 0.865, r"$\sup_{x}\;|F_n(x) - F(x)| \;\to\; 0$   almost surely",
                        ha="center", fontsize=17, color=style.MUTED)

    # left panel ---------------------------------------------------------
    grid = np.linspace(*X_RANGE, 600)
    ax.plot(grid, norm.cdf(grid), color=style.BLUE, label=r"$F$  (truth)")
    (step,) = ax.step([], [], where="post", color=style.YELLOW, label=r"$F_n$  (from data)")
    (gap,) = ax.plot([], [], color=style.RED, lw=3.2, solid_capstyle="round")
    rug = ax.vlines([], 0, 0, color=style.YELLOW, alpha=0.5, lw=0.8)
    n_text = ax.text(0.03, 0.93, "", transform=ax.transAxes, fontsize=17)
    d_text = ax.text(0.03, 0.85, "", transform=ax.transAxes, fontsize=15, color=style.RED)
    ax.set_xlim(*X_RANGE)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(r"$x$")
    ax.legend(loc="lower right", fontsize=14)

    # right panel --------------------------------------------------------
    for d in d_other:
        ax2.plot(ns, d, color=style.MUTED, alpha=0.18, lw=1)
    (path,) = ax2.plot([], [], color=style.YELLOW, lw=2.4)
    (dot,) = ax2.plot([], [], "o", color=style.RED, ms=7)
    ref = ax2.plot(ns, 0.9 / np.sqrt(ns), "--", color=style.GREEN, lw=1.6, alpha=0)[0]
    ref_label = ax2.text(2.3, 0.9 / np.sqrt(2.3) * 1.45, r"$\propto 1/\sqrt{n}$",
                         color=style.GREEN, fontsize=15, alpha=0)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(1, N_MAX * 1.1)
    ax2.set_ylim(0.008, 1.05)
    ax2.set_xlabel(r"$n$")
    ax2.set_title(r"$D_n = \sup_x |F_n(x) - F(x)|$", fontsize=15, pad=10)

    caption = fig.text(0.5, 0.022, "", ha="center", fontsize=14, color=style.MUTED)

    n_intro, n_outro = int(INTRO * fps), int(OUTRO * fps)
    total = n_intro + n_grow + n_outro

    def draw_n(n: int):
        data = np.sort(sample[:n])
        xs = np.concatenate([[X_RANGE[0]], data, [X_RANGE[1]]])
        ys = np.concatenate([[0.0], np.arange(1, n + 1) / n, [1.0]])
        step.set_data(xs, ys)
        x_star, fn_val, f_val = argsup_distance(sample[:n], norm.cdf)
        gap.set_data([x_star, x_star], [f_val, fn_val])
        segs = [[(v, -0.05), (v, -0.01)] for v in data[:: max(1, n // 400)]]
        rug.set_segments(segs)
        k = np.searchsorted(ns, n)
        path.set_data(ns[: k + 1], d_main[: k + 1])
        dot.set_data([n], [d_main[k]])
        n_text.set_text(rf"$n = {n}$")
        d_text.set_text(rf"$D_n = {d_main[k]:.3f}$")

    def update(i: int):
        if i < n_intro:
            draw_n(1)
            caption.set_text(r"One sample  $X_1, X_2, X_3, \dots$  from $\mathcal{N}(0, 1)$.  "
                             r"Watch what happens as $n$ grows.")
        elif i < n_intro + n_grow:
            draw_n(int(frame_ns[i - n_intro]))
            caption.set_text(r"Yellow: our sample (one $\omega$).   Grey: 40 other samples (other $\omega$'s).")
        else:
            draw_n(N_MAX)
            a = min(1.0, (i - n_intro - n_grow) / (0.4 * fps))
            ref.set_alpha(0.9 * a)
            ref_label.set_alpha(a)
            caption.set_text(r"The simulation shows finitely many $\omega$ and $n$.  "
                             "'Almost surely' and the limit need the proof (Borel–Cantelli).")
        return step, gap, path, dot

    return fig, update, total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "media")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--preview", action="store_true", help="only save a few PNG frames")
    parser.add_argument("--no-gif", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    stem = "ep03_glivenko_cantelli"

    fig, update, total = build(args.fps)
    if args.preview:
        for i in [0, total // 5, total // 2, int(total * 0.8), total - 1]:
            update(i)
            fig.savefig(args.out / f"{stem}_frame{i:04d}.png")
        return

    anim = FuncAnimation(fig, update, frames=total, blit=False)
    anim.save(args.out / f"{stem}.mp4", writer=FFMpegWriter(fps=args.fps, bitrate=4000))
    if not args.no_gif:
        fig_g, update_g, total_g = build(12)
        fig_g.set_dpi(55)
        FuncAnimation(fig_g, update_g, frames=total_g).save(
            args.out / f"{stem}.gif", writer=PillowWriter(fps=12))


if __name__ == "__main__":
    main()
