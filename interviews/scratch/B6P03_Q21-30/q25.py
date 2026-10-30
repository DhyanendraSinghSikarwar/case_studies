# Q25 near-duplicate leakage: MinHash demo and re-evaluation (illustrative numbers)
import hashlib, random
import numpy as np

# 1) The reported accuracy decomposed (invented split of correct answers)
N, exact, near, acc = 5000, 300, 1550, 0.92
print(f"exact {exact/N:.0%}, near-dup {near/N:.0%}, clean docs {N-near}")
assert exact / N == 0.06 and near / N == 0.31 and N - near == 3450
correct = round(N * acc)                     # 4600 correct
acc_near = 0.98                              # assume the model is right on 98% of the near-dups
correct_near = round(near * acc_near)        # 1519
acc_clean = (correct - correct_near) / (N - near)
print(f"correct overall {correct}; near-dup correct {correct_near}; accuracy on clean docs {acc_clean:.1%}")
assert correct == 4600 and correct_near == 1519 and round(acc_clean, 3) == 0.893
# sensitivity: if near-dups are only right 95% of the time
for a in (0.95, 0.98, 1.00):
    print(f"  near-dup accuracy {a:.0%} -> clean accuracy {(correct - near*a)/(N-near):.1%}")

# 2) Exact hashing misses a one-word edit; MinHash does not
def shingles(text, k=3):
    w = text.split(); return {" ".join(w[i:i+k]) for i in range(len(w) - k + 1)}
def jaccard(a, b): return len(a & b) / len(a | b)
rng = random.Random(25)
vocab = [f"w{i}" for i in range(500)]
base = [rng.choice(vocab) for _ in range(200)]
edited = base.copy(); edited[50] = "changed"; edited[120] = "edit"
d1, d2 = " ".join(base), " ".join(edited)
print("exact hash equal:", hashlib.md5(d1.encode()).hexdigest() == hashlib.md5(d2.encode()).hexdigest())
assert hashlib.md5(d1.encode()).hexdigest() != hashlib.md5(d2.encode()).hexdigest()
s1, s2 = shingles(d1), shingles(d2)
true_j = jaccard(s1, s2)
M = 256
P = 2**61 - 1
a = [rng.randrange(1, P) for _ in range(M)]; b = [rng.randrange(0, P) for _ in range(M)]
def sig(S):
    hs = [int(hashlib.md5(x.encode()).hexdigest()[:15], 16) for x in S]
    return np.array([min((ai * h + bi) % P for h in hs) for ai, bi in zip(a, b)])
est = float((sig(s1) == sig(s2)).mean())
print(f"true Jaccard {true_j:.3f}, MinHash estimate ({M} hashes) {est:.3f}")
assert true_j > 0.9 and abs(est - true_j) < 0.08
# an unrelated document
other = " ".join(rng.choice(vocab) for _ in range(200))
est_o = float((sig(s1) == sig(shingles(other))).mean())
print(f"unrelated doc: MinHash estimate {est_o:.3f}")
assert est_o < 0.1

# 3) Uncertainty on the clean-subset accuracy
n = N - near; k = correct - correct_near
p = k / n; half = 1.96 * (p * (1 - p) / n) ** 0.5
print(f"clean accuracy {p:.1%} +- {half:.1%} (95%)")
assert half < 0.011
