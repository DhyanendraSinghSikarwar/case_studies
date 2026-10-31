import subprocess
import sys
import time

# 1. Collisions are resolved by probing and then comparing keys with ==
class K:
    def __init__(self, v): self.v = v
    def __hash__(self): return 0               # every key collides
    def __eq__(self, o): return self.v == o.v

d = {K(i): i for i in range(5)}
print("1) all-collide dict still correct:", d[K(3)], len(d), K(9) in d)
assert d[K(3)] == 3 and len(d) == 5 and K(9) not in d

# 2. hash(-1) == hash(-2)
print("2) hash(-1) =", hash(-1), "| hash(-2) =", hash(-2), "| hash(-3) =", hash(-3))
assert hash(-1) == hash(-2) == -2
print("   small ints hash to themselves:", [hash(i) for i in (0, 1, 2, 1000)])
M = 2**61 - 1                                  # CPython int hash modulus on 64-bit builds
print("   int hash is x mod (2**61 - 1): hash(M) =", hash(M), ", hash(M + 5) =", hash(M + 5), ", hash(-M - 1) =", hash(-M - 1))
assert sys.hash_info.modulus == M and hash(M) == 0 and hash(M + 5) == 5

# 3. str hashes change between runs; int hashes do not
def run(seed, expr):
    out = subprocess.run([sys.executable, "-P", "-c", f"print({expr})"], env={"PYTHONHASHSEED": seed},
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()
s1, s2, s3 = run("1", "hash('apple')"), run("2", "hash('apple')"), run("1", "hash('apple')")
i1, i2 = run("1", "hash(12345)"), run("2", "hash(12345)")
print("3) hash('apple') under seed 1 vs seed 2 equal?", s1 == s2, "| seed 1 twice equal?", s1 == s3)
print("   hash(12345) under seed 1 vs 2:", i1, i2)
assert s1 != s2 and s1 == s3 and i1 == i2 == "12345"
print("   str ordering of a set can differ between runs:",
      run("1", "list({'a','b','c','d','e'})") != run("2", "list({'a','b','c','d','e'})"))

# 4. Adversarial inputs: real ints that all collide (no custom class needed)
keys = [i * M for i in range(1, 6)]
print("4) hashes of 1*M..5*M:", [hash(k) for k in keys])
assert all(hash(k) == 0 for k in keys)

# 5. Insertion cost with a constant __hash__ vs a normal hash (sandbox timings, not proof of big-O)
class Const:
    __slots__ = ()
    def __hash__(self): return 0               # no __eq__: default identity compare, done in C

class Normal:
    __slots__ = ()                             # default hash from id(): spreads well

def build(cls, n):
    objs = [cls() for _ in range(n)]
    t = time.perf_counter()
    s = set()
    for o in objs:
        s.add(o)
    return time.perf_counter() - t

print("5) insert n keys into a set (sandbox-only timings, seconds):")
print("   n      constant-hash   normal-hash")
rows = []
for n in (625, 1250, 2500, 5000):
    tc, tn = min(build(Const, n) for _ in range(3)), min(build(Normal, n) for _ in range(3))
    rows.append((n, tc, tn))
    print(f"   {n:<6} {tc:12.5f}   {tn:12.5f}")
growth = rows[-1][1] / rows[0][1]
print(f"   constant-hash time grew about {growth:.0f}x for 8x the keys; the normal hash grew about {rows[-1][2] / rows[0][2]:.0f}x")
assert growth > 12                              # far above linear (8x); quadratic would be ~64x
