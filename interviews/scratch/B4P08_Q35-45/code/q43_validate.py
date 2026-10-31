import yaml, sys
s = yaml.safe_load(open(sys.argv[1]))
for k in ["logging", "data_quality_gates", "drift", "performance", "fairness", "alert_tiers", "retraining", "shadow_challenger"]:
    assert k in s, k
assert s["performance"]["matured_cohort_days"] >= s["performance"]["label_delay_days"]["max"]
assert {t["tier"] for t in s["alert_tiers"]} == {"page", "ticket", "info"}
assert s["retraining"]["rollback"] and "shadow_challenger_14_days" in s["retraining"]["gate"]
print("spec OK:", len(s["data_quality_gates"]), "gates,", len(s["alert_tiers"]), "alert tiers, matured cohort", s["performance"]["matured_cohort_days"], "days")

