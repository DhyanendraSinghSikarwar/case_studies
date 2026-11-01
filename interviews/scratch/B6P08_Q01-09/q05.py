# Q5: mocked feature store -> 12 minutes of 100% errors. Illustrative.
rps = 600
detect_to_rollback_start_s = 12 * 60          # errors from deploy until the engineer starts the rollback
rollback_s = 6 * 60                           # rollback takes 6 more minutes
failed_first_12 = rps * detect_to_rollback_start_s
assert failed_first_12 == 432_000
# upper bound: errors continue at 100% until the rollback finishes
failed_total_upper = rps * (detect_to_rollback_start_s + rollback_s)
assert failed_total_upper == 648_000 and 12 + 6 == 18
print("failed requests, first 12 min:", failed_first_12, "| through end of rollback (upper bound):", failed_total_upper)

# against an illustrative 99.9% monthly availability objective at constant 600 rps, 30 days
month_req = rps * 86_400 * 30
budget_req = month_req * 0.001
print("monthly requests:", month_req, "| error budget (0.1%):", int(budget_req))
assert month_req == 1_555_200_000 and int(budget_req) == 1_555_200
print("share of monthly budget burned:", round(failed_total_upper / budget_req, 3))
assert round(failed_total_upper / budget_req, 3) == 0.417

# what would a gate have cost? Canary 5% of traffic, auto rollback when error rate > 5% for 60 s,
# rollback takes 6 minutes but only the canary share is exposed
canary_share = 0.05
detect_s = 60
canary_failed = rps * canary_share * (detect_s + rollback_s)
print("canary exposure (failed requests):", int(canary_failed))
assert int(canary_failed) == 12_600
print("reduction vs no canary:", round(1 - canary_failed / failed_total_upper, 3))
assert round(1 - canary_failed / failed_total_upper, 3) == 0.981

# smoke test with a REAL (staging) feature store would have failed the first request
def feature_store_mock(key): return {"f1": 0.0}            # always happy
def feature_store_real(key): raise KeyError("feature view 'f_v2' not found")   # what production did (invented)
def predict(fetch):
    feats = fetch("user42"); return feats["f1"]
assert predict(feature_store_mock) == 0.0                   # CI: green
try:
    predict(feature_store_real); raise SystemExit("should fail")
except KeyError as e:
    print("contract/smoke test against the real store fails at once:", e)
