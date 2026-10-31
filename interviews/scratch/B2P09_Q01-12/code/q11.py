# Is 82% vs 80% on 200 cases a real gain? Wilson CI, unpaired z, exact McNemar, paired bootstrap.
import math, random
from math import comb
random.seed(8)

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = p + z*z/(2*n)
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (c - h) / d, (c + h) / d
print("old 160/200 Wilson 95%:", tuple(round(x, 3) for x in wilson(160, 200)))
print("new 164/200 Wilson 95%:", tuple(round(x, 3) for x in wilson(164, 200)))

# unpaired two-proportion z-test (ignores that both prompts saw the same cases)
p1, p2 = 160/200, 164/200; pp = (160+164)/400
z = (p2 - p1) / math.sqrt(pp*(1-pp)*(2/200)); pval = math.erfc(abs(z)/math.sqrt(2))
print(f"unpaired z={z:.2f}, p={pval:.2f}")

def mcnemar_exact(b, c):               # two-sided exact binomial on discordant pairs, p0 = 0.5
    d = b + c; k = min(b, c)
    return min(1.0, 2 * sum(comb(d, i) for i in range(k + 1)) / 2**d)
def mcnemar_brute(b, c):               # enumerate all 2^d sign patterns
    d = b + c; k = min(b, c); tail = 0
    for mask in range(2**d):
        ones = bin(mask).count("1")
        if min(ones, d - ones) <= k: tail += 1
    return tail / 2**d
for b, c in ((4, 0), (6, 2), (7, 3)):
    assert abs(mcnemar_exact(b, c) - mcnemar_brute(b, c)) < 1e-12
print("exact McNemar matches brute-force enumeration: OK")

def paired_boot(b, c, n=200, reps=4000):          # cases where new wins = b, old wins = c
    diffs = [0]*(n-b-c) + [1]*b + [-1]*c
    out = sorted(sum(random.choice(diffs) for _ in range(n)) / n for _ in range(reps))
    return out[int(.025*reps)], out[int(.975*reps)]
print("same +4 net wins, different overlap (b = new-only wins, c = old-only wins):")
for b, c in ((4, 0), (6, 2), (14, 10), (34, 30)):
    lo, hi = paired_boot(b, c)
    print(f"  b={b:2d} c={c:2d} discordant={b+c:2d} McNemar p={mcnemar_exact(b, c):.3f} paired-bootstrap 95% CI for diff=({lo:+.3f}, {hi:+.3f})")

# power: true rates new-only win 7%, old-only win 5% (assumed), n=200, exact McNemar at p<0.05
def power(n=200, pb=0.07, pc=0.05, reps=3000):
    hit = 0
    for _ in range(reps):
        b = c = 0
        for _ in range(n):
            r = random.random()
            if r < pb: b += 1
            elif r < pb + pc: c += 1
        hit += (b + c > 0) and mcnemar_exact(b, c) < 0.05
    return hit / reps
print("simulated power to detect a true +2 point gain with n=200:", round(power(), 2))
