# TOY: pinning check (a dated suffix means pinned: crude SYNTHETIC rule), and a regression check on paired results with an exact sign test (verified by brute force).
import re, math, itertools, random
DATED = re.compile(r"-\d{4}-\d{2}-\d{2}$")
def check_pin(model): return "pinned" if DATED.search(model) else "UNPINNED alias"
for m in ["acme-large-latest", "acme-large-2026-03-01", "acme-large"]: print(f"{m:24} {check_pin(m)}")
# deprecation calendar (SYNTHETIC dates): days left before a pinned snapshot retires
from datetime import date
retire = {"acme-large-2026-03-01": date(2027, 2, 1)}
today = date(2026, 10, 24)
for m, d in retire.items(): print(m, "retires in", (d - today).days, "days -> start migration runbook if under 120")
# exact one-sided sign test on discordant pairs: candidate worse than old on b items, better on c items
def sign_p_worse(b, c):            # P(X >= b) under Binomial(b+c, 0.5): evidence that candidate is worse
    n = b + c
    return sum(math.comb(n, k) for k in range(b, n + 1)) / 2 ** n
def brute(b, c):
    n = b + c; hits = 0
    for bits in itertools.product([0, 1], repeat=n): hits += sum(bits) >= b
    return hits / 2 ** n
for b, c in [(8, 2), (5, 5), (12, 4), (3, 0)]:
    assert abs(sign_p_worse(b, c) - brute(b, c)) < 1e-12
    print(f"worse on {b}, better on {c}: p = {sign_p_worse(b, c):.4f}")
print("closed form matches brute force for all four cases")
# toy models on 60 regression cases: new snapshot has a format regression on 10 percent of cases (SYNTHETIC)
random.seed(5)
old = [random.random() < 0.85 for _ in range(60)]
new = [o and (random.random() > 0.15) or (not o and random.random() < 0.3) for o in old]
b = sum(o and not n for o, n in zip(old, new)); c = sum(n and not o for o, n in zip(old, new))
print(f"old pass {sum(old)}/60 new pass {sum(new)}/60 | new worse on {b}, better on {c}, p = {sign_p_worse(b, c):.4f}")
