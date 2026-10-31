import difflib
import numpy as np
from math import sqrt
from collections import Counter

searches, zr = 1_000_000, 0.06
zero = searches * zr
n, spell_k, missing_k = 500, 200, 100
print("zero-result searches/day", zero)
assert zero == 60_000
sp, mi = spell_k / n, missing_k / n
oth = 1 - sp - mi
proj = {"spelling/synonym": zero * sp, "genuinely missing": zero * mi, "other": zero * oth}
print({k: round(v) for k, v in proj.items()}, "| other share", round(oth, 2))
assert proj["spelling/synonym"] == 24_000 and proj["genuinely missing"] == 12_000 and round(proj["other"]) == 24_000
for name, k in (("spelling/synonym", spell_k), ("missing", missing_k)):
    p = k / n; se = sqrt(p * (1 - p) / n)
    print(f"{name}: share {p:.0%} +- {1.96*se:.3f} -> searches/day {zero*(p-1.96*se):,.0f} to {zero*(p+1.96*se):,.0f}")
assert round(zero * (0.4 - 1.96 * sqrt(0.4 * 0.6 / 500))) == 21424
# effect of fixing a share of the spelling group
for fix in (0.5, 0.8):
    fixed = proj["spelling/synonym"] * fix
    print(f"fix {fix:.0%} of the spelling group -> {fixed:,.0f} searches now return results; zero-result rate {(zero-fixed)/searches:.2%}")
assert (zero - 12_000) / searches == 0.048 and (zero - 19_200) / searches == 0.0408
# a correction that helps nobody if it is wrong: precision matters. Toy vocabulary + difflib
vocab = ["running shoes", "wireless headphones", "phone charger", "yoga mat", "water bottle", "laptop stand"]
queries = ["runing shoes", "wireles headphones", "fone charger", "yoga mat", "kettlebell", "lap top stand", "trainers"]
for q in queries:
    m = difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)
    print(f"{q!r:24} -> {m[0] if m else None}")
fixed = [q for q in queries if difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)]
assert "runing shoes" in fixed and "fone charger" in fixed and "kettlebell" not in fixed and "trainers" not in fixed   # string similarity cannot fix a synonym or a missing product
# missing-product signal with a privacy threshold: count distinct users, publish only if >= k
rng = np.random.default_rng(40)
terms = ["kettlebell 16kg", "cast iron dutch oven", "left handed scissors", "rare vinyl X", "jane doe address"]
log = []
for t, cnt, users in (("kettlebell 16kg", 900, 600), ("cast iron dutch oven", 400, 250), ("left handed scissors", 120, 90), ("rare vinyl X", 15, 4), ("jane doe address", 6, 1)):
    uids = rng.integers(0, users, cnt)
    log += [(t, int(u)) for u in uids]
cnt = Counter(t for t, u in log); du = {t: len({u for tt, u in log if tt == t}) for t in cnt}
K = 20
pub = [t for t in cnt if du[t] >= K]
print({t: (cnt[t], du[t]) for t in cnt})
print("published to sellers (>= 20 distinct users):", pub)
assert "jane doe address" not in pub and "rare vinyl X" not in pub and len(pub) == 3
