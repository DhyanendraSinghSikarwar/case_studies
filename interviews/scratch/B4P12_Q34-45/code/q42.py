# Q42: feature usage audit on an invented lineage table.
features = [f"f{i:03d}" for i in range(1, 21)]
model_uses = {"churn_v3": {"f001","f002","f003","f004","f005","f006"}}
declared_consumers = {"f001": {"churn_v3"}, "f002": {"churn_v3"}, "f003": {"churn_v3"}, "f004": {"churn_v3"}, "f005": {"churn_v3"}, "f006": {"churn_v3"}, "f010": {"retention_dash"}}
# read log (who actually reads which feature), invented
reads = [("churn_v3", f) for f in model_uses["churn_v3"]] + [("retention_dash", "f010"), ("promo_svc", "f003"), ("promo_svc", "f011"), ("fin_report", "f011")]
actual = {}
for who, f in reads: actual.setdefault(f, set()).add(who)
unused = [f for f in features if f not in actual]
undeclared = {f: sorted(actual[f] - declared_consumers.get(f, set())) for f in actual if actual[f] - declared_consumers.get(f, set())}
print(f"features {len(features)}, read by anyone {len(actual)}, unused {len(unused)}")
print("unused:", unused)
print("undeclared consumers:", undeclared)
assert "f011" in undeclared and "f003" in undeclared and "f020" in unused
# delete order: unused first, then risk by (consumers undeclared) -> do not delete; declare them
print("delete first (no readers):", unused[:5], "...; DO NOT delete f003/f011 until promo_svc/fin_report declared")
