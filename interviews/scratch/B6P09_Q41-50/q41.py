# Q41: uniqueness on quasi-identifiers (prompt numbers) + a synthetic generalisation demo (invented data)
import numpy as np
from collections import Counter

records, combos, singles = 50_000, 4_000, 600
print("share of RECORDS unique   :", singles / records)        # what the question asks
print("share of COMBINATIONS that are unique:", singles / combos)  # a different base, easy to confuse
rest_records, rest_combos = records - singles, combos - singles
print("other records / combos     :", rest_records, rest_combos, "avg group", round(rest_records / rest_combos, 2))
assert singles / records == 0.012 and singles / combos == 0.15
assert rest_records == 49_400 and rest_combos == 3_400

# Synthetic illustration only (NOT the prompt's data): how banding changes uniqueness and k.
rng = np.random.default_rng(7)
n = 50_000
age = np.clip(rng.normal(52, 18, n).round(), 0, 99).astype(int)
area = rng.zipf(1.6, n) % 400            # 3-digit-like area codes, skewed: a few big, many tiny
sex = rng.integers(0, 2, n)

def stats(keys):
    c = Counter(keys)
    sizes = np.array(list(c.values()))
    smallest = min(sizes)
    uniq = int((sizes == 1).sum())
    k5_fail = int(sizes[sizes < 5].sum())   # records sitting in groups smaller than 5
    return len(c), uniq, uniq / n, k5_fail / n, smallest

raw = stats(zip(age, area, sex))
band = stats(zip(age // 10, area, sex))               # 10-year bands
band2 = stats(zip(age // 10, area // 10, sex))        # plus coarser area (2-digit style)
for name, s in [("raw age/area/sex", raw), ("10y age band", band), ("10y band + coarser area", band2)]:
    print(f"{name:26} combos={s[0]:5d} unique_records={s[1]:5d} unique_share={s[2]:.3f} share_in_groups_lt5={s[3]:.3f}")
assert raw[2] > band[2] > band2[2] or band[2] >= band2[2] and raw[2] > band2[2]
assert band2[3] < raw[3]
# suppression: drop the records still in groups smaller than 5 and re-check
keys = list(zip(age // 10, area // 10, sex))
c = Counter(keys)
kept = [k for k in keys if c[k] >= 5]
c2 = Counter(kept)
print("after suppressing small groups: records kept", len(kept), "min group", min(c2.values()))
assert min(c2.values()) >= 5
