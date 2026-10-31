# Percentile bootstrap CI for accuracy, and paired bootstrap for A-B, on synthetic per-case 0/1 outcomes.
import random, math
random.seed(5)
n = 200
# synthetic (assumed): A and B correlated (B is correct on most cases A is)
A, B = [], []
for _ in range(n):
    easy = random.random() < 0.72
    a = 1 if easy or random.random() < 0.36 else 0
    b = 1 if (easy and random.random() < 0.97) or (not easy and random.random() < 0.28) else 0
    A.append(a); B.append(b)
def boot_ci(x, B_=10000, alpha=0.05, seed=1):
    r = random.Random(seed); m = len(x)
    stats = sorted(sum(x[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))
    return stats[int(alpha / 2 * B_)], stats[int((1 - alpha / 2) * B_) - 1]
def paired_boot(a, b, B_=10000, seed=2):
    r = random.Random(seed); m = len(a); d = [x - y for x, y in zip(a, b)]
    stats = sorted(sum(d[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))   # resample CASES, keep pairs together
    return sum(d) / m, stats[int(0.025 * B_)], stats[int(0.975 * B_) - 1]
def unpaired_boot(a, b, B_=10000, seed=3):
    r = random.Random(seed); m = len(a)
    stats = sorted(sum(a[r.randrange(m)] for _ in range(m)) / m - sum(b[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))
    return stats[int(0.025 * B_)], stats[int(0.975 * B_) - 1]
pa, pb = sum(A) / n, sum(B) / n
lo, hi = boot_ci(A)
print(f"A accuracy {pa:.3f}  bootstrap 95% CI [{lo:.3f}, {hi:.3f}]  width {hi-lo:.3f}")
print(f"  normal-approx check: +-1.96*sqrt(p(1-p)/n) = {1.96*math.sqrt(pa*(1-pa)/n):.3f}  (half-width of bootstrap: {(hi-lo)/2:.3f})")
d, plo, phi = paired_boot(A, B)
ulo, uhi = unpaired_boot(A, B)
bc = sum(1 for a, b in zip(A, B) if a == 1 and b == 0); cc = sum(1 for a, b in zip(A, B) if a == 0 and b == 1)
print(f"B accuracy {pb:.3f}; diff A-B {d:+.3f}")
print(f"paired bootstrap 95% CI   [{plo:+.3f}, {phi:+.3f}]  width {phi-plo:.3f}")
print(f"unpaired bootstrap 95% CI [{ulo:+.3f}, {uhi:+.3f}]  width {uhi-ulo:.3f}   (wrongly ignores the pairing)")
se = math.sqrt(bc + cc - (bc - cc) ** 2 / n) / n
print(f"closed-form paired SE from discordant counts (A only right {bc}, B only right {cc}): {se:.4f}; 1.96*SE = {1.96*se:.3f} vs bootstrap half-width {(phi-plo)/2:.3f}")
print("CI excludes 0 (paired)?", plo > 0 or phi < 0, "| (unpaired)?", ulo > 0 or uhi < 0)
