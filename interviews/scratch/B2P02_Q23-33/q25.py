import random, hashlib
def shingles(t, k=3):
    w = t.split(); return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)}
def h(s, seed): return int(hashlib.md5(f"{seed}|{s}".encode()).hexdigest()[:8], 16)
def minhash(sh, n=128): return [min(h(s, i) for s in sh) for i in range(n)]
def est(a, b): return sum(x == y for x, y in zip(a, b)) / len(a)
a = "the quick brown fox jumps over the lazy dog near the river bank today and then runs home fast"
b = "the quick brown fox jumps over the lazy dog near the river bank today and then walks home slowly"
A, B = shingles(a), shingles(b)
print("exact Jaccard:", round(len(A & B)/len(A | B), 3))
for n in (16, 128, 1024):
    print(n, "perms -> estimate:", round(est(minhash(A, n), minhash(B, n)), 3))
# LSH banding: collision prob for Jaccard s with b bands of r rows = 1-(1-s^r)^b
for s in (0.3, 0.5, 0.8, 0.9):
    print("s=%.1f P(candidate)=%.3f" % (s, 1-(1-s**8)**16))
