"""Usage: release_notes.py OLD.json NEW.json OLD_TAG NEW_TAG [--commits FILE]"""
import json
import sys

LOWER_IS_BETTER = {"p95_latency_ms", "brier", "log_loss", "rmse"}


def verdict(name, delta):
    if abs(delta) < 1e-12:
        return "same"
    better = delta < 0 if name in LOWER_IS_BETTER else delta > 0
    return "better" if better else "WORSE"


def render(old, new, old_tag, new_tag, commits=()):
    out = [f"# {new['model']} v{new['version']} ({new_tag})", ""]
    out += ["| Field | Value |", "|---|---|",
            f"| Model version | {new['version']} |",
            f"| Data version | {new['data_version']} (was {old['data_version']}) |",
            f"| Git SHA | {new['git_sha']} |",
            f"| Rollback target | {old['model']} v{old['version']} ({old_tag}) |", ""]
    out += ["## Metrics versus previous champion", "",
            "| Metric | Old | New | Change | Verdict |", "|---|---|---|---|---|"]
    for k in sorted(new["metrics"]):
        n = new["metrics"][k]
        o = old["metrics"].get(k)
        if o is None:
            out.append(f"| {k} | n/a | {n:.3f} | n/a | new metric |")
            continue
        d = n - o
        out.append(f"| {k} | {o:.3f} | {n:.3f} | {d:+.3f} | {verdict(k, d)} |")
    out += ["", f"## What changed ({old_tag}..{new_tag})", ""]
    out += [f"- {c}" for c in commits] or ["- (no commit list supplied)"]
    out += ["", "## Known limitations", ""]
    out += [f"- {x}" for x in new.get("limitations", [])] or ["- none recorded (fill this in, do not leave it empty)"]
    return "\n".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    commits = []
    if "--commits" in args:
        i = args.index("--commits")
        commits = [l.strip() for l in open(args[i + 1]) if l.strip()]
        del args[i:i + 2]
    old = json.load(open(args[0])); new = json.load(open(args[1]))
    print(render(old, new, args[2], args[3], commits))
