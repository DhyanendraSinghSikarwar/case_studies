# Q13: sticky 5% canary by hashing user id + shadow mode. Model A = logistic regression, model B = decision tree (iris).
import hashlib, statistics, time
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)
A = LogisticRegression(max_iter=500).fit(X, y)
B = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)

def bucket(user_id: str) -> int:           # stable 0..99, same user -> same bucket, on every pod
    return int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100

def route(user_id: str, canary_pct: int = 5) -> str:
    return "B" if bucket(user_id) < canary_pct else "A"

# 1) stickiness and share
users = [f"user-{i}" for i in range(20000)]
first = {u: route(u) for u in users}
assert all(route(u) == first[u] for u in users), "assignment must be sticky"
share = sum(v == "B" for v in first.values()) / len(users)
print(f"sticky: yes (20000 users, routed twice, identical)")
print(f"share routed to B: {share:.3%} (target 5%; hash gives about 5%, not exactly 5%)")
print("bucket('user-1') =", bucket("user-1"), "-> route:", route("user-1"))

# 2) shadow: every request is answered by A; B also scores a copy, nothing from B reaches the user
rng = np.random.default_rng(0)
rows = X[rng.integers(0, len(X), 3000)] + rng.normal(0, 0.15, (3000, 4))   # noisy traffic
agree, lat_a, lat_b = 0, [], []
for r in rows:
    r = r.reshape(1, -1)
    t = time.perf_counter(); pa = A.predict(r)[0]; lat_a.append(time.perf_counter() - t)
    t = time.perf_counter(); pb = B.predict(r)[0]; lat_b.append(time.perf_counter() - t)
    agree += int(pa == pb)                  # logged only; the user got pa
print(f"shadow agreement A vs B: {agree/len(rows):.3%} over {len(rows)} requests")
d = (statistics.median(lat_b) - statistics.median(lat_a)) * 1000
print(f"median latency B minus A: {d:+.3f} ms (this sandbox only, in-process sklearn, not a benchmark)")
