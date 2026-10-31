# A Python mirror of the ci-ok rule, to hand-check the truth table. It is NOT the GitHub evaluator.
def ci_ok(results):
    return not any(r in ("failure", "cancelled") for r in results)

cases = [
    ("docs-only PR: lint success, model-gate skipped", ["success", "skipped"]),
    ("model PR, all green", ["success", "success"]),
    ("model-gate failure", ["success", "failure"]),
    ("lint cancelled", ["cancelled", "success"]),
]
for name, r in cases:
    print(f"{name:50s} -> {'mergeable' if ci_ok(r) else 'blocked'}")
