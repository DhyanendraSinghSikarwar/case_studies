"""Map changed file paths to a GitHub Actions matrix JSON for a monorepo of models."""
import json, sys

SHARED_PREFIXES = ("libs/", "ci/", "pyproject.toml", "requirements")   # a change here tests every model
ALL_MODELS = ["churn", "fraud", "ltv"]

def matrix(changed):
    hit = set()
    for p in changed:
        if p.startswith(SHARED_PREFIXES):
            return {"include": [{"model": m, "reason": "shared"} for m in ALL_MODELS]}
        parts = p.split("/")
        if parts[0] == "models" and len(parts) > 2 and parts[1] in ALL_MODELS:
            hit.add(parts[1])
    return {"include": [{"model": m, "reason": "changed"} for m in sorted(hit)]}

if __name__ == "__main__":
    changed = [l.strip() for l in sys.stdin if l.strip()]
    print(json.dumps(matrix(changed), separators=(",", ":")))
