# Q25 chest X-ray scanner gap (illustrative numbers)
from math import sqrt
nA, nB, prev = 8_000, 2_000, 0.10
posA, posB = nA * prev, nB * prev
assert posA == 800 and posB == 200 and nA + nB == 10_000
sA, sB = 0.88, 0.71
tpA, tpB = posA * sA, posB * sB
missA, missB = posA - tpA, posB - tpB
assert round(tpA) == 704 and round(tpB) == 142 and round(missA) == 96 and round(missB) == 58
overall = (tpA + tpB) / (posA + posB)
assert abs(overall - 0.846) < 1e-9
print(f"overall sensitivity {overall:.1%}; missed A={missA:.0f} B={missB:.0f}; B share of misses {missB/(missA+missB):.0%} with 20% of images")

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
loA, hiA = wilson(tpA, posA); loB, hiB = wilson(tpB, posB)
assert hiB < loA   # intervals do not overlap
print(f"A {loA:.1%}-{hiA:.1%}, B {loB:.1%}-{hiB:.1%}")
se = sqrt(sA*(1-sA)/posA + sB*(1-sB)/posB)
z = (sA - sB) / se
assert 4.9 < z < 5.1
print(f"gap 17 points, z={z:.1f}")

# If B had A's sensitivity it would miss this many fewer
extra = posB * (sA - sB)
assert round(extra) == 34
print(f"abnormal scans on B that A-level sensitivity would have caught: {extra:.0f}")

# Abnormal cases needed to estimate sensitivity of the new scanner within +-5 points (95%), assume 0.8
need_pos = 1.96**2 * 0.8 * 0.2 / 0.05**2
images = need_pos / prev
assert 245 < need_pos < 247 and 2_450 < images < 2_470
print(f"abnormal cases needed {need_pos:.0f} -> about {images:,.0f} images at 10% abnormal")
