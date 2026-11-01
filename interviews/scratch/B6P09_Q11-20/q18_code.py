import numpy as np

n, fake, flagged, tp = 500, 60, 150, 54
precision, recall = tp / flagged, tp / fake
assert precision == 0.36 and recall == 0.90
p = fake / n
se = np.sqrt(p * (1 - p) / n)
lo, hi = p - 1.96 * se, p + 1.96 * se
assert p == 0.12 and abs(se - 0.014532) < 1e-5
assert round(lo, 3) == 0.092 and round(hi, 3) == 0.148
assert n * p >= 10 and n * (1 - p) >= 10          # normal approximation is reasonable
print("fake share", p, "95% interval", round(float(lo), 3), round(float(hi), 3))
print("precision", precision, "recall", recall, "flag rate", flagged / n)

def wilson(k, m, z=1.96):
    ph = k / m
    c = (ph + z * z / (2 * m)) / (1 + z * z / m)
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / (1 + z * z / m)
    return c - h, c + h
pl, ph_ = wilson(tp, flagged); rl, rh = wilson(tp, fake)
print("precision 95% (Wilson)", round(float(pl), 3), round(float(ph_), 3))
print("recall 95% (Wilson)", round(float(rl), 3), round(float(rh), 3))
assert pl < precision < ph_ and rl < recall < rh

# Cost of a blanket takedown of flagged reviews, scaled to an illustrative 1,000,000 reviews
reviews = 1_000_000
flag_n = reviews * flagged / n
wrong = flag_n * (1 - precision)
print("flagged", int(flag_n), "genuine reviews taken down", int(wrong), "fake reviews missed", round(reviews * 0.12 * (1 - recall)))
assert int(flag_n) == 300_000 and int(wrong) == 192_000

# Review queue: if humans check flagged reviews, how many fake per 100 checked vs random review?
print("fake per 100 reviews checked: flagged", 100 * precision, "random", 100 * p)
assert 100 * precision == 36 and abs(100 * precision / (100 * p) - 3.0) < 1e-9     # 3x lift over random
