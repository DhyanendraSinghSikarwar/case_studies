import sys; sys.path.insert(0, ".")
from rollout import Promotion
OK = {"requests": 5000, "error_rate": 0.002, "p99_ms": 120, "psi": 0.05}
for title, seq in [
    ("good candidate", [{"smoke_passed": True}, OK, {**OK, "requests": 400}, OK]),
    ("bad canary", [{"smoke_passed": True}, OK, {**OK, "p99_ms": 480}]),
]:
    p = Promotion()
    print("==", title)
    for m in seq:
        v = p.step(m)
        print(f"  {p.log[-1][0]:8s} {v:8s} {p.log[-1][2]}")
    print("  final:", p.stage, p.state)
