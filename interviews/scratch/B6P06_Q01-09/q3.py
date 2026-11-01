import math
apps, appr = 50_000, 30_000
assert appr == apps * 0.6
d_lr, d_gb = appr * 0.040, appr * 0.036
avoided = d_lr - d_gb
loss = avoided * 2500
print(f"defaults: logistic {d_lr:.0f}, boosted {d_gb:.0f}, fewer {avoided:.0f}, loss avoided {loss:,.0f}")
assert (round(d_lr), round(d_gb), round(avoided), round(loss)) == (1200, 1080, 120, 300000)
# is a 0.4pp gap real on 30,000 approvals? (unpaired, conservative)
se = math.sqrt(.04*.96/appr + .036*.964/appr)
lo, hi = 0.004 - 1.96*se, 0.004 + 1.96*se
print(f"gap 0.40pp, 95% CI ({lo*100:.2f}, {hi*100:.2f}) pp -> loss avoided range {lo*appr*2500:,.0f} to {hi*appr*2500:,.0f}")
assert 0.0008 < lo < 0.001 and 0.0070 < hi < 0.0072
# break-even: yearly cost of the explanation layer that would erase the saving
print("break-even extra cost of keeping boosted model compliant:", f"{loss:,.0f}")
assert loss == 300_000
# a middle option capturing half the gap (e.g. logistic with binned features)
half = loss / 2
print("middle option capturing half the gap:", f"{half:,.0f}")
assert half == 150_000
