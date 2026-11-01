cust, churners, flagged, tp = 100_000, 5_000, 1_000, 300
base = churners / cust
prec, rec = tp / flagged, tp / churners
lift = prec / base
print(f"base rate {base:.1%}, precision {prec:.0%}, recall {rec:.0%}, lift {lift:.1f}x")
assert base == 0.05 and prec == 0.30 and abs(rec - 0.06) < 1e-12 and abs(lift - 6) < 1e-9
# random pick of 1,000 customers would catch
rand_tp = flagged * base
print(f"a random 1,000 would contain {rand_tp:.0f} churners; the model finds {tp}")
assert rand_tp == 50
# illustrative economics: offer costs 5, saves 20% of churners reached, a saved customer is worth 100
cost, save, value = 5.0, 0.20, 100.0
be_prec = cost / (save * value)
net_model = tp*save*value - flagged*cost
net_rand = rand_tp*save*value - flagged*cost
print(f"break-even precision {be_prec:.0%}; net value: model {net_model:,.0f}, random {net_rand:,.0f}")
assert abs(be_prec - 0.25) < 1e-12 and net_model == 1000 and net_rand == -4000
# recall is capped by capacity: even a perfect list of 1,000 would reach 1,000/5,000
print(f"max recall with 1,000 contacts: {flagged/churners:.0%}")
assert flagged/churners == 0.20
