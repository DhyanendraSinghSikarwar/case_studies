import hashlib, math, random

class Bloom:
    def __init__(self, m, k):
        self.m, self.k, self.bits = m, k, bytearray(m)   # one byte per bit: simple, 8x wasteful
    def _idx(self, item):
        d = hashlib.sha256(item.encode()).digest()       # deterministic, unlike str hash()
        return [int.from_bytes(d[4*i:4*i+4], "big") % self.m for i in range(self.k)]  # k <= 8
    def add(self, item):
        for i in self._idx(item): self.bits[i] = 1
    def __contains__(self, item):
        return all(self.bits[i] for i in self._idx(item))

def predicted(m, n, k): return (1 - math.exp(-k * n / m)) ** k

m, n, k = 10_000, 1_000, 3
rng = random.Random(42)
members = [f"https://ex.test/in/{rng.getrandbits(48):012x}" for _ in range(n)]
others  = [f"https://ex.test/out/{rng.getrandbits(48):012x}" for _ in range(20_000)]
exact = set(members)                       # brute force: exact, but stores every URL
assert not (exact & set(others))

bf = Bloom(m, k)
for u in members: bf.add(u)
assert all(u in bf for u in members)       # no false negatives, ever
fp = sum(u in bf for u in others)
print(f"m={m} n={n} k={k}")
print(f"predicted FPR = {predicted(m, n, k):.4f}")
print(f"measured  FPR = {fp / len(others):.4f}  ({fp} of {len(others)} absent URLs said 'seen')")
print(f"fraction of bits set = {sum(bf.bits)/m:.3f}  (theory 1-e^(-kn/m) = {1-math.exp(-k*n/m):.3f})")

kopt = m / n * math.log(2)
print(f"optimal k = (m/n) ln2 = {kopt:.2f}; predicted FPR at k=7: {predicted(m, n, 7):.4f}")
bf7 = Bloom(m, 7)
for u in members: bf7.add(u)
fp7 = sum(u in bf7 for u in others)
print(f"measured FPR at k=7 = {fp7 / len(others):.4f}")

# sizing for the prompt: 1e8 URLs, target 1% false positives
N, p = 10**8, 0.01
bits = -N * math.log(p) / math.log(2) ** 2
print(f"1e8 URLs at p=1%: {bits/N:.2f} bits/item, {bits/8/1e6:.0f} MB, k={bits/N*math.log(2):.1f}")

# seeded cross-check: no false negatives on many random configurations
for seed in range(300):
    r = random.Random(seed)
    mm, nn, kk = r.randint(8, 200), r.randint(0, 30), r.randint(1, 8)
    b = Bloom(mm, kk); items = [f"x{r.getrandbits(32)}" for _ in range(nn)]
    for it in items: b.add(it)
    assert all(it in b for it in items)
print("300 seeded configs: zero false negatives")

# edge cases
empty = Bloom(100, 3)
assert "anything" not in empty
tiny = Bloom(1, 3); tiny.add("a")
assert "zzz" in tiny                       # m=1: everything is a false positive
print("edge asserts passed")
