# Standalone, stdlib only. Part 1: unbiased pass@k estimator with exact tests. Part 2: a MOCK execution verifier (subprocess + timeout).
import math, random, subprocess, sys, tempfile, os

def pass_at_k(n, c, k):                        # unbiased estimator: 1 - C(n-c, k) / C(n, k)
    if n - c < k: return 1.0                   # fewer than k failures: every size-k subset has a pass
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

# exact tiny cases
assert pass_at_k(4, 1, 2) == 0.5               # 1 - C(3,2)/C(4,2) = 1 - 3/6
assert pass_at_k(4, 0, 2) == 0.0 and pass_at_k(4, 4, 2) == 1.0 and pass_at_k(5, 2, 1) == 2 / 5
print("pass@2 with n=4, c=1:", pass_at_k(4, 1, 2), "| pass@1 with n=5, c=2:", pass_at_k(5, 2, 1))

# unbiasedness by brute force: average over ALL size-k subsets of the n samples of "does the subset contain a pass"
from itertools import combinations
n, c, k = 8, 2, 3; flags = [1] * c + [0] * (n - c)
exact = sum(any(s) for s in combinations(flags, k)) / math.comb(n, k)
print(f"n=8 c=2 k=3: formula {pass_at_k(n, c, k):.6f}  brute-force subsets {exact:.6f}")

# naive plug-in estimate 1-(1-c/n)^k is biased; the unbiased one matches the true pass@k on average (synthetic problem with p=0.2)
random.seed(0); p, n, k, T = 0.2, 10, 5, 100000; true = 1 - (1 - p) ** k
un = nv = 0.0
for _ in range(T):
    c = sum(random.random() < p for _ in range(n)); un += pass_at_k(n, c, k); nv += 1 - (1 - c / n) ** k
print(f"true pass@5 {true:.4f} | unbiased mean {un/T:.4f} | naive plug-in mean {nv/T:.4f}")

# ---- MOCK verifier: run candidate code against unit tests in a separate process with a time limit ----
TESTS = "assert add(2, 3) == 5\nassert add(-1, 1) == 0\n"
CANDS = {"correct": "def add(a, b):\n    return a + b\n",
         "wrong": "def add(a, b):\n    return a - b\n",
         "hangs": "def add(a, b):\n    while True:\n        pass\n"}
def run_tests(code, timeout=2):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.py"); open(path, "w").write(code + "\n" + TESTS)
        try: return subprocess.run([sys.executable, "-I", path], capture_output=True, timeout=timeout, cwd=d).returncode == 0
        except subprocess.TimeoutExpired: return False
res = {k_: run_tests(v) for k_, v in CANDS.items()}
print("verifier results:", res, "-> preference pair (chosen=correct, rejected=wrong); RLVR reward = 1.0 / 0.0")
