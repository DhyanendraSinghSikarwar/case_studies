# Retrain-vs-patch economics (all illustrative, in Rs lakh)
loss_per_day = 2.0
retrain_days = 14
patch_live_day = 1                       # patch live after 1 day, so day 1 is unprotected
build_cost = 1.5                         # patch build and test cost
recover_frac = 0.50                      # share of the daily loss the patch removes (assumption)
side_cost = 0.2                          # extra cost per day from crude rules (e.g. wrongly declined good customers)

wait_loss = loss_per_day * retrain_days
assert wait_loss == 28.0
days_protected = retrain_days - patch_live_day
net_daily = loss_per_day * recover_frac - side_cost
benefit = days_protected * net_daily - build_cost
print(f"wait for retrain: lose {wait_loss:.1f} lakh over {retrain_days} days")
print(f"patch: protected {days_protected} days, net {net_daily:.2f} lakh/day, benefit after build cost = {benefit:.2f} lakh")
assert abs(benefit - 8.9) < 1e-9

# Break-even recovery fraction: days_protected * (loss*r - side) = build_cost
r_star = (build_cost / days_protected + side_cost) / loss_per_day
print(f"break-even recovery fraction: {r_star:.3f}")
assert abs(r_star - 0.1577) < 0.001

print("recovery  net benefit (lakh)")
for r in (0.10, 0.20, 0.30, 0.50, 0.70):
    b = days_protected * (loss_per_day * r - side_cost) - build_cost
    print(f"{r:8.0%}  {b:8.2f}")
# Worst case: patch recovers only 20% and side cost is twice as large
worst = days_protected * (loss_per_day * 0.2 - 0.4) - build_cost
print(f"worst case (20% recovery, side cost 0.4/day): {worst:.2f} lakh")
assert worst < 0
# Retirement rule: switch the patch off when the retrained model beats model+patch on matured shadow data
# (the patch is also deleted from code on a fixed date, e.g. retrain day + 7)
