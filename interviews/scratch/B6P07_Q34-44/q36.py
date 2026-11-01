import math

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
k_dev, k_rom, n = 160, 104, 200
r_dev, r_rom = k_dev / n, k_rom / n
gap = r_dev - r_rom
rel = gap / r_dev
print(f"recall@5 Devanagari {r_dev:.0%}, romanised {r_rom:.0%}; gap {gap*100:.0f} points; relative drop {rel:.0%}; romanised = {r_rom/r_dev:.0%} of Devanagari")
assert r_dev == 0.80 and r_rom == 0.52 and round(gap, 2) == 0.28 and round(rel, 2) == 0.35

# Is 28 points more than noise? (two-proportion z, unpaired)
pool = (k_dev + k_rom) / (2 * n)
z = gap / math.sqrt(pool * (1 - pool) * 2 / n)
lo_d, hi_d = wilson(k_dev, n); lo_r, hi_r = wilson(k_rom, n)
print(f"z = {z:.1f}; Wilson Devanagari [{lo_d:.3f}, {hi_d:.3f}], romanised [{lo_r:.3f}, {hi_r:.3f}]")
assert z > 5 and hi_r < lo_d   # intervals do not overlap

# Why exact-token match fails on romanised text: spelling is not standardised.
# Toy example (invented words): three common romanised spellings of the same Hindi word.
variants = ["kaise", "kaisey", "kese"]
def grams(w, n=3):
    w = f"^{w}$"
    return {w[i:i + n] for i in range(len(w) - n + 1)}
def jac(a, b): return len(a & b) / len(a | b)
exact = [[a == b for b in variants] for a in variants]
print("exact-match hits among different spellings:", sum(exact[i][j] for i in range(3) for j in range(3) if i != j))
sims = [round(jac(grams(variants[i]), grams(variants[j])), 2) for i in range(3) for j in range(i + 1, 3)]
print("char-trigram Jaccard between spellings:", sims)
assert sum(exact[i][j] for i in range(3) for j in range(3) if i != j) == 0 and max(sims) > 0.5 and min(sims) < 0.2   # n-grams rescue near spellings only

# Guardrail: Devanagari non-regression. Allow at most 2 points of loss (illustrative) on 200 queries
# would not be detectable at n = 200: the 95% half-width is about 5-6 points.
print("Devanagari half-width at n=200: %.3f" % ((hi_d - lo_d) / 2))
assert 0.05 < (hi_d - lo_d) / 2 < 0.06

# Example: blended recall if 40% of traffic is romanised (illustrative share)
blend0 = 0.6 * r_dev + 0.4 * r_rom
blend1 = 0.6 * r_dev + 0.4 * 0.70
print(f"blended recall {blend0:.3f} -> {blend1:.3f} (gain {100*(blend1-blend0):.1f} points)")
assert round(blend0, 3) == 0.688 and round(blend1, 3) == 0.76 and round(100 * (blend1 - blend0), 1) == 7.2
