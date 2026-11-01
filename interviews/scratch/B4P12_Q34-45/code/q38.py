# Q38: tiered forecasting compute policies; invented table. Units abstract.
tiers = {  # share of series, cost per series-run (compute units), stock-out cost per series per period at current policy
 "A_fast":  dict(n=2000,  cost=10.0, so=50.0),
 "B_mid":   dict(n=8000,  cost=10.0, so=8.0),
 "C_tail":  dict(n=40000, cost=10.0, so=0.5),
}
runs_per_month = 4
base_cost = sum(t["n"] * t["cost"] * runs_per_month for t in tiers.values())
# policy: (cost multiplier per tier, relative stock-out increase per tier)
policies = {
 "P1 retrain all less often (4->2/mo)": {"A_fast": (0.5, 0.10), "B_mid": (0.5, 0.10), "C_tail": (0.5, 0.10)},
 "P2 tail -> global/cheap model":        {"A_fast": (1.0, 0.0),  "B_mid": (1.0, 0.0),  "C_tail": (0.15, 0.20)},
 "P3 tiered: A as-is, B 2/mo, tail cheap + 1/mo": {"A_fast": (1.0, 0.0), "B_mid": (0.5, 0.05), "C_tail": (0.15 * 0.5, 0.25)},
}
print(f"base compute {base_cost:.0f}; base stock-out cost {sum(t['n']*t['so'] for t in tiers.values()):.0f} per period")
best = None
for name, p in policies.items():
    comp = sum(tiers[k]["n"] * tiers[k]["cost"] * runs_per_month * p[k][0] for k in tiers)
    extra = sum(tiers[k]["n"] * tiers[k]["so"] * p[k][1] for k in tiers)
    saved = base_cost - comp
    print(f"{name:50s} saved {saved/base_cost*100:5.1f}%  extra stock-out {extra:8.0f}  saved per extra {saved/max(extra,1):6.2f}  meets 40%: {saved/base_cost>=0.40}")
    if saved / base_cost >= 0.40 and (best is None or extra < best[1]): best = (name, extra)
print("pick:", best[0])
