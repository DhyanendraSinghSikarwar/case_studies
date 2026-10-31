# Q42: a rules fallback never exercised; a renamed config key made it fail 100% (invented example)
import json, random

# Production config AFTER someone renamed 'rule_threshold' -> 'rules.score_cutoff'
prod_config = {"rules": {"score_cutoff": 620}, "model_url": "svc://credit"}
# The fallback was written against the old name
REQUIRED_KEYS = ["rule_threshold"]

def fallback_decide(app, cfg):
    return "approve" if app["bureau_score"] >= cfg["rule_threshold"] else "refer"

# 1) Unit test with a hand-written fixture passes: false comfort
stale_fixture = {"rule_threshold": 620}
assert fallback_decide({"bureau_score": 700}, stale_fixture) == "approve"

# 2) A contract test that loads the REAL config fails at deploy time, not 14 months later
def contract_test(cfg, required):
    return [k for k in required if k not in cfg]
missing = contract_test(prod_config, REQUIRED_KEYS)
print("contract test, missing keys:", missing)
assert missing == ["rule_threshold"]

# 3) Without any exercise, every call fails: show 100% errors and who notices
errors = 0
for i in range(1000):
    try:
        fallback_decide({"bureau_score": 600 + i % 200}, prod_config)
    except KeyError:
        errors += 1
print("fallback errors on 1000 calls:", errors, "= 100%")
assert errors == 1000

# 4) Detection delay: dormant 14 months vs a synthetic probe every 5 minutes vs 1% live traffic
months_dormant_days = 14 * 30
probe_min = 5
rps, share = 200, 0.01
print("days undetected:", months_dormant_days, "| probe detects within", probe_min, "min")
print("1% live canary of the fallback path:", rps * share, "calls/s -> one call every",
      round(1 / (rps * share), 1), "s on average, so a broken path shows up in seconds")
assert months_dormant_days == 420 and rps * share == 2.0 and round(1 / (rps * share), 1) == 0.5

# 5) Fix: fallback reads config through one validated loader with a schema; test against real file
def load_fallback_cfg(cfg):
    cut = cfg.get("rules", {}).get("score_cutoff")
    if not isinstance(cut, int):
        raise ValueError("fallback config invalid: rules.score_cutoff")
    return {"cutoff": cut}
def fallback_decide_v2(app, fcfg):
    return "approve" if app["bureau_score"] >= fcfg["cutoff"] else "refer"
fcfg = load_fallback_cfg(prod_config)
assert fallback_decide_v2({"bureau_score": 700}, fcfg) == "approve"
try:
    load_fallback_cfg({"rules": {}}); raise SystemExit("should have failed")
except ValueError as e:
    print("loader fails loudly at start-up:", e)

# 6) Game-day gate: staged blast radius, abort rule decided before starting
stages = [("staging, 100%", 1.0), ("prod shadow, 0% decisions", 0.0), ("prod canary 1%", 0.01), ("prod 10% off-peak", 0.10)]
abort_error_rate = 0.02
def stage_ok(observed_error_rate): return observed_error_rate <= abort_error_rate
print("abort if error rate above", abort_error_rate, "->", [stage_ok(x) for x in (0.0, 0.01, 0.05)])
assert [stage_ok(x) for x in (0.0, 0.01, 0.05)] == [True, True, False]
print("stages:", [s for s, _ in stages])
