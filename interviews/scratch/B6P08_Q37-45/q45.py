# Q45: bug on 3% of requests carrying 20% of revenue, started 90 minutes ago (invented numbers)
req_share, rev_share, age_min = 0.03, 0.20, 90
value_ratio = rev_share / req_share
print("revenue per affected request vs average:", round(value_ratio, 2), "x")
assert round(value_ratio, 2) == 6.67

# Money at stake (illustrative revenue: 2,400,000 units per day, flat across the day)
rev_per_day = 2_400_000
rev_per_min = rev_per_day / (24 * 60)
at_risk_per_hour = rev_per_min * 60 * rev_share
print("revenue/hour:", rev_per_min * 60, "| carried by affected requests/hour:", at_risk_per_hour)
assert rev_per_min * 60 == 100_000 and at_risk_per_hour == 20_000
loss_frac = 0.5                    # assume half of the affected revenue is actually lost (invented)
lost_so_far = at_risk_per_hour * (age_min / 60) * loss_frac
print("lost so far at 50% loss rate:", lost_so_far)
assert lost_so_far == 15_000

# Why nobody noticed for 90 minutes: an overall alert on error rate misses a 3% slice
overall_alert = 0.05                   # alert at 5% overall error rate
print("overall error rate from the bug:", req_share, "-> alert fires:", req_share >= overall_alert)
assert not (req_share >= overall_alert)
rev_weighted_alert = 0.05              # same threshold on a revenue-weighted error rate
print("revenue-weighted error rate:", rev_share, "-> alert fires:", rev_share >= rev_weighted_alert)
assert rev_share >= rev_weighted_alert
# detection delay if checked every 5 min on the weighted metric, with a 3-point window: <= 10 min
check_min, consecutive = 5, 2
print("detection delay: hourly dashboard up to 60 min vs 5-min check needing", consecutive, "breaches =", check_min * consecutive, "min")
assert check_min * consecutive == 10

# Option cost, remaining loss at the same 50% loss rate (invented ETAs)
per_min = at_risk_per_hour * loss_frac / 60
options = {"rollback (verified last good)": 20, "manual workaround (route segment to rules)": 30,
           "forward fix (code, test, deploy)": 180}
for name, eta in options.items():
    print(f"{name:45} ETA {eta:3} min  extra loss {per_min * eta:8.0f}")
assert round(per_min * 20) == 3333 and round(per_min * 180) == 30000
assert per_min * 20 < per_min * 30 < per_min * 180

# Decision rule written as code
def decide(deploy_in_window, last_good_exists, rollback_verified, segment_identifiable):
    if deploy_in_window and last_good_exists and rollback_verified:
        return "rollback"
    if segment_identifiable:
        return "manual workaround, then fix forward"
    return "fix forward with all hands; escalate"
assert decide(True, True, True, True) == "rollback"
assert decide(True, True, False, True) == "manual workaround, then fix forward"
assert decide(False, False, False, False).startswith("fix forward")
print("decisions:", decide(True, True, True, True), "|", decide(True, True, False, True))

# Severity by revenue-weighted impact (the thresholds are an illustrative policy, not a standard)
def sev(rev_share_hit):
    return "SEV1" if rev_share_hit >= 0.10 else "SEV2" if rev_share_hit >= 0.02 else "SEV3"
print("severity:", sev(rev_share), "(by revenue) vs", sev(req_share), "(by request share)")
assert sev(rev_share) == "SEV1" and sev(req_share) == "SEV2"

# Update cadence and who runs what (4 teams on one rota)
roles = {"incident commander": "rota A", "ops lead (does the fix/rollback)": "ML on-call",
         "comms lead": "rota B", "scribe": "rota C", "liaison, data/platform": "rota D"}
assert len(roles) == 5
print("update every 30 min; escalate to executive if no mitigation by", 60, "min after declaring")
