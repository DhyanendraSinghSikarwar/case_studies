#!/usr/bin/env python3
"""Promotion gate. Exit 0 = promote allowed, 1 = blocked. Thresholds are example policy values."""
import argparse, json, sys

POLICY = {"auc_floor": 0.80, "max_auc_drop": 0.005, "max_p95_ms": 50.0, "max_size_mb": 200.0,
          "slice_floor": 0.70, "max_slice_drop": 0.02}
REQUIRED = ["auc", "p95_ms", "size_mb", "slices", "signature"]

def load(path):
    try:
        with open(path) as f:
            return json.load(f) or None
    except FileNotFoundError:
        return None

def check(cand, champ, allow_no_champion=False, p=POLICY):
    rows = []                                     # (check, status, reason)
    def add(name, ok, why): rows.append((name, "PASS" if ok else "FAIL", why))
    missing = [k for k in REQUIRED if k not in (cand or {})]
    if missing:                                   # a missing metric is a failure, never a pass
        add("metrics present", False, "candidate missing: " + ", ".join(missing))
        return rows
    add("metrics present", True, "all required keys found")
    add("auc floor", cand["auc"] >= p["auc_floor"], f"{cand['auc']:.3f} vs floor {p['auc_floor']}")
    add("latency budget", cand["p95_ms"] <= p["max_p95_ms"], f"p95 {cand['p95_ms']} ms vs {p['max_p95_ms']}")
    add("size budget", cand["size_mb"] <= p["max_size_mb"], f"{cand['size_mb']} MB vs {p['max_size_mb']}")
    worst = min(cand["slices"].items(), key=lambda kv: kv[1])
    add("slice floor", worst[1] >= p["slice_floor"], f"worst slice {worst[0]}={worst[1]:.3f} vs {p['slice_floor']}")
    if champ is None or "auc" not in champ:
        ok = allow_no_champion
        add("champion metrics", ok, "none found; " + ("first release, relative checks skipped" if ok
                                                    else "fail closed (use --allow-no-champion for the first release)"))
        return rows
    drop = champ["auc"] - cand["auc"]
    add("vs champion auc", drop <= p["max_auc_drop"], f"drop {drop:+.3f} (max {p['max_auc_drop']})")
    for s, v in champ.get("slices", {}).items():
        d = v - cand["slices"].get(s, 0.0)
        if d > p["max_slice_drop"]:
            add(f"slice {s} vs champion", False, f"drop {d:+.3f} (max {p['max_slice_drop']})")
    add("signature", cand["signature"] == champ.get("signature"), "inputs match champion" if
        cand["signature"] == champ.get("signature") else f"{cand['signature']} != {champ.get('signature')}")
    return rows

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True); ap.add_argument("--champion", required=True)
    ap.add_argument("--allow-no-champion", action="store_true")
    a = ap.parse_args(argv)
    rows = check(load(a.candidate), load(a.champion), a.allow_no_champion)
    print(f"{'check':24}{'result':8}reason")
    for n, s, w in rows: print(f"{n:24}{s:8}{w}")
    failed = [r for r in rows if r[1] == "FAIL"]
    print("GATE:", "BLOCKED (%d failed)" % len(failed) if failed else "PASSED")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
