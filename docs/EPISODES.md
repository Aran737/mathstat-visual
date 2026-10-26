# Episode plan — Chapters 1 and 2

Every episode follows the same five beats:

1. **Statement** — in my own words, with the formula.
2. **Intuition** — two sentences, no symbols.
3. **Prediction** — written down *before* rendering. Surprises mark gaps in understanding.
4. **Animation** — one script in `episodes/`, logic in `src/mathstat/`, correctness in `tests/`.
5. **What the simulation cannot show** — and which proof step does that job instead.

Colour roles (fixed for the whole series, see `src/mathstat/style.py`):
blue = truth, yellow = estimate from data, red = error, green = bounds.

| # | Topic | Lecture | Status |
|---|---|---|---|
| 01 | Strong law of large numbers | 1.1 | open |
| 02 | The empirical distribution | Def. 2.1, (2.1) | open |
| 03 | Glivenko–Cantelli | Def. 2.2, Thm. 2.1 | **done** (reference episode) |
| 04 | Shatter coefficients | Def. 2.3, Remark a–d, Ex. 2.1 a | open |
| 05 | Intersections and quadrants | Ex. 2.1 b | open |
| 06 | The VC inequality, step by step | Thm. 2.2 | open |
| 07 | From a bound to "almost surely" | Cor. 2.3 | open |

---

## 01 · Strong law of large numbers

**Statement.** For i.i.d. integrable X₁, X₂, … the running mean (X₁ + … + Xₙ)/n converges to E X for almost every ω.

**Animation idea.** 30 paths of the running mean for exponential data, converging into a narrowing band around E X. Then the same for the Cauchy distribution (no expectation): the paths never settle and keep jumping.

**Predict first.** Which paths jump the most, early or late ones? What happens to Cauchy at n = 10 000?

**Library.** `empirical.running_mean`

**Cannot show.** "Almost every ω" — we see 30. The Cauchy failure shows *why* integrability is an assumption.

## 02 · The empirical distribution

**Statement.** μₙ puts mass 1/n on each data point; repeated values collect several units of 1/n. For each fixed set B, μₙ(B) → μ(B) almost surely.

**Animation idea.** Points drop onto the line as little stacks (height = mass). A fixed set B is highlighted; a counter shows μₙ(B) approaching μ(B).

**Predict first.** Is μₙ a probability measure for every n? What changes if two points coincide?

**Library.** `empirical.empirical_measure`, `empirical.point_masses`

**Cannot show.** This is for *one fixed* B. Doing it for all B at once is a much stronger claim — that is what Episodes 03–07 are about.

## 03 · Glivenko–Cantelli ✅

See `episodes/ep03_glivenko_cantelli.py`. Use it as the template for the others.

## 04 · Shatter coefficients

**Statement.** s(𝒜, n) is the largest number of different subsets that sets from 𝒜 can cut out of n points. Always 1 ≤ s(𝒜, n) ≤ 2ⁿ, and it is non-decreasing in n.

**Animation idea.** n points on a line; an interval slides and stretches, every new subset it cuts out lights up in a growing gallery. Then a growth plot: half-lines (n + 1), intervals (n(n+1)/2 + 1), and 2ⁿ on a log scale.

**Predict first.** Can intervals cut out {x₁, x₃} without x₂? For which n does 2ⁿ overtake n(n+1)/2 + 1 for good?

**Library.** `shatter.traces_halflines`, `shatter.traces_intervals`, `shatter.shatter_coefficient_1d`, `shatter.is_shattered`

**Cannot show.** The maximum over *all* point configurations. Write down why distinct points in d = 1 are enough (ties only merge traces) — that argument is the actual justification for the code.

## 05 · Intersections and quadrants

**Statement.** If 𝒜 = {A₁ ∩ A₂}, then s(𝒜, n) ≤ s(𝒜₁, n) · s(𝒜₂, n). For lower-left quadrants in ℝᵈ this gives s(𝒜, n) ≤ (n + 1)ᵈ.

**Animation idea.** Random points in the plane; a quadrant corner (−∞, z] moves over a grid of positions, each new trace is counted. The count is compared to (n + 1)². Then: intervals as half-line ∩ half-line, with the product bound next to the exact count.

**Predict first.** How far below (n + 1)² is the actual count? Does it depend on how the points are placed?

**Library.** `shatter.traces_quadrants`, `shatter.traces_intersection`

**Cannot show.** The proof is a counting argument, not a statement about randomness — the animation shows it on examples, the proof shows it for all.

## 06 · The VC inequality, step by step

**Statement.** P(sup_A |μₙ(A) − μ(A)| > ε) ≤ 8 · s(𝒜, n) · exp(−nε²/32).

**Animation idea.** Four panels, one per proof step. In each, estimate *both sides* of that step's inequality by Monte Carlo and show "left ≤ right":

1. symmetrisation with a ghost sample X′₁, …, X′ₙ,
2. random signs U₁, …, Uₙ,
3. conditioning on the Xᵢ and the union bound over at most s(𝒜, n) patterns,
4. Hoeffding.

Final panel: the true probability vs. the bound as n grows. The bound is above 1 (useless) for a long time.

**Predict first.** Which step loses the most? For half-lines and ε = 0.1, from which n on is the bound below 1?

**Library.** `bounds.hoeffding_bound`, `bounds.vc_bound`, `bounds.chebyshev_bound`

**Cannot show.** Every check is for a few n and ε. Also note the "w.l.o.g. n ≥ 8/ε²" at the start of the proof — show what goes wrong in Step 1 without it.

## 07 · From a bound to "almost surely"

**Statement.** If log s(𝒜, n) / n → 0, then sup_A |μₙ(A) − μ(A)| → 0 almost surely.

**Animation idea.** Two contrasting classes:

* half-lines: log(n + 1)/n → 0, the supremum dies out;
* **all finite sets**: s(𝒜, n) = 2ⁿ, so log s / n = log 2 does not go to 0. For continuous μ, the sample itself is a finite set with μₙ = 1 but μ = 0 — the supremum stays at **1 forever**.

**Predict first.** Before running: what is sup over all finite sets of |μₙ(A) − μ(A)| for n = 5? For n = 5 000?

**Cannot show.** The step from "summable probabilities" to "almost surely" is Borel–Cantelli. A simulation can show the summands getting small; it cannot show the series converges or what happens on a null set.
