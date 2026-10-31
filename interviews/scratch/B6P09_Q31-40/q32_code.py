import numpy as np
from math import comb, sqrt

flagged, audited, fraud_s, cap = 1000, 100, 40, 200
p = fraud_s / audited
proj = flagged * p
weeks = flagged / cap
print("sample rate", p, "| projected fraudulent among flagged", proj, "| weeks to clear", weeks)
assert p == 0.4 and proj == 400 and weeks == 5

# uncertainty on the 40 of 100 (the audit is a sample)
z = 1.96
se = sqrt(p * (1 - p) / audited)
lo, hi = p - z * se, p + z * se
fpc = sqrt((flagged - audited) / (flagged - 1))
se2 = se * fpc
print("normal 95% interval:", round(lo, 3), "to", round(hi, 3), "-> sellers", round(lo * flagged), "to", round(hi * flagged),
      "| with finite-population correction", round((p - z * se2) * flagged), "to", round((p + z * se2) * flagged))
assert round(lo * flagged) == 304 and round(hi * flagged) == 496

# random review order: first week = 200 reviewed out of 1000 with K fraudulent (hypergeometric)
K = 400
mean1 = cap * K / flagged
sd1 = sqrt(cap * (K / flagged) * (1 - K / flagged) * (flagged - cap) / (flagged - 1))
print("week 1, random order: mean", mean1, "sd", round(sd1, 2))
assert mean1 == 80 and round(sd1, 2) == 6.20
for Kx in (304, 496):
    print("  if true K =", Kx, "-> week-1 mean", cap * Kx / flagged)

# ordering by score: invented audit table, 100 audited sellers split by model-score tertile
tiers = {"high score": (30, 21), "mid score": (35, 13), "low score": (35, 6)}   # (audited, fraud)
assert sum(a for a, f in tiers.values()) == 100 and sum(f for a, f in tiers.values()) == 40
rates = {k: f / a for k, (a, f) in tiers.items()}
print({k: round(v, 3) for k, v in rates.items()})
# project to 1000 flagged in the same tier shares (audited share = 30/35/35 percent)
size = {k: a * 10 for k, (a, f) in tiers.items()}
fr = {k: size[k] * rates[k] for k in tiers}
print("tier sizes", size, "| projected fraud", {k: round(v) for k, v in fr.items()}, "total", round(sum(fr.values())))
assert abs(sum(fr.values()) - 400) < 1e-9
# week 1 by score order: all 200 from high tier (300 sellers) + nothing else needed
wk1_score = cap * rates["high score"]
print("week 1 reviewing the high tier first: expected fraud found", wk1_score, "vs random", mean1)
assert wk1_score == 140
# value-ordered: add dollars at risk per seller (invented) -> expected loss per reviewer-hour
rng = np.random.default_rng(32)
exposure = rng.lognormal(7, 1, flagged)               # invented exposure per seller
pr = np.concatenate([np.full(300, .70), np.full(350, .3714), np.full(350, .1714)])
rng.shuffle(pr)
by_p = np.argsort(-pr)[:cap]
by_ev = np.argsort(-(pr * exposure))[:cap]
print("week-1 expected fraud caught: by probability", round(pr[by_p].sum(), 1), "| by probability x exposure", round(pr[by_ev].sum(), 1))
print("week-1 expected loss stopped: by probability", round((pr * exposure)[by_p].sum()), "| by probability x exposure", round((pr * exposure)[by_ev].sum()))
assert (pr * exposure)[by_ev].sum() >= (pr * exposure)[by_p].sum()
assert pr[by_p].sum() >= pr[by_ev].sum()
