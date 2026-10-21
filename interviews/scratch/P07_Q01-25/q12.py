import numpy as np
rng = np.random.default_rng(0)
n = 200_000
rel = rng.random(n) < 0.3                       # true relevance (A: 0.5 CTR if seen, B: ...)
true_rel = rng.uniform(0.1, 0.6, n)             # item attractiveness
pos = rng.integers(1, 6, n)                     # logged position 1..5 (random for clarity)
exam = 1 / pos                                  # examination propensity
click = rng.random(n) < true_rel * exam
# naive CTR by position-blind item group: items shown at pos1 vs pos5
for p in (1, 5):
    m = pos == p
    print(f"pos {p}: naive CTR {click[m].mean():.3f}  (true mean relevance {true_rel[m].mean():.3f})")
# IPW estimate of relevance: click / propensity
for p in (1, 5):
    m = pos == p
    print(f"pos {p}: IPW relevance  {(click[m] / exam[m]).mean():.3f}")
