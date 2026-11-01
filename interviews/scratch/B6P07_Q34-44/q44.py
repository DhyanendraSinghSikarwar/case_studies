import math
from scipy import stats

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
n, k0, k1 = 200, 90, 140
r0, r1 = k0 / n, k1 / n
print(f"corrected: {r0:.0%} -> {r1:.0%}; change {100*(r1-r0):.0f} percentage points; extra corrected prompts {k1-k0}; relative change {r1/r0-1:.0%}")
assert r0 == 0.45 and r1 == 0.70 and round(100 * (r1 - r0)) == 25 and k1 - k0 == 50

lo0, hi0 = wilson(k0, n); lo1, hi1 = wilson(k1, n)
print(f"Wilson 95%: before [{lo0:.3f}, {hi0:.3f}], after [{lo1:.3f}, {hi1:.3f}]")
assert hi0 < lo1   # intervals do not overlap

# Paired view on the same 200 prompts. Net change +50 = c - b where b = corrected before but not after, c = the reverse.
# Invented split of the discordant prompts: b = 10, c = 60.
b, c = 10, 60
assert k0 - b + c == k1 and c - b == 50
z = (c - b) / math.sqrt(b + c)
print(f"McNemar z = {z:.2f}, two-sided p = {2*stats.norm.sf(z):.1e} (b = {b}, c = {c})")
assert z > 5
# Without the paired counts, the unpaired comparison is already clear for a 25-point gain
pool = (k0 + k1) / (2 * n)
zu = (r1 - r0) / math.sqrt(pool * (1 - pool) * 2 / n)
print(f"unpaired z = {zu:.2f}")
assert zu > 5

# Why thumbs-up can reward the old behaviour. Invented rates: users thumbs-up 70% of answers that go along
# with their premise and 55% of answers that correct it.
up_agree, up_correct = 0.70, 0.55
before = r0 * up_correct + (1 - r0) * up_agree
after = r1 * up_correct + (1 - r1) * up_agree
print(f"thumbs-up rate before {before:.4f}, after {after:.4f}: change {100*(after-before):.2f} points while correction rose 25 points")
assert round(before, 4) == 0.6325 and round(after, 4) == 0.595 and after < before
