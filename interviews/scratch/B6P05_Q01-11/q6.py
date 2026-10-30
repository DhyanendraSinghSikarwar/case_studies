N, fraud_rate, loss = 1_000_000, 0.005, 80
flag, tp, review, fp_cost = 20_000, 3_500, 2, 5
frauds = int(N * fraud_rate)
fp = flag - tp
prec, rec = tp / flag, tp / frauds
print(f"frauds {frauds:,}; flagged {flag:,}; true positives {tp:,}; false positives {fp:,}")
print(f"precision {prec:.1%}; recall {rec:.1%}")
assert frauds == 5000 and fp == 16500 and abs(prec - 0.175) < 1e-12 and abs(rec - 0.70) < 1e-12
cost_without = frauds * loss
missed = (frauds - tp) * loss
rev_cost = flag * review
fp_total = fp * fp_cost
cost_with = missed + rev_cost + fp_total
print(f"without model {cost_without:,}; with model: missed {missed:,} + review {rev_cost:,} + false-alarm {fp_total:,} = {cost_with:,}; saving {cost_without-cost_with:,}")
assert (cost_without, missed, rev_cost, fp_total, cost_with) == (400000, 120000, 40000, 82500, 242500)
assert cost_without - cost_with == 157500
# break-even false-alarm cost per flagged genuine customer
be_fp = (tp * loss - rev_cost) / fp
print(f"break-even false-alarm cost {be_fp:.2f} per flagged genuine customer (assumed 5)")
assert abs(be_fp - 14.5455) < 1e-3
# break-even fraud loss
be_loss = (rev_cost + fp_total) / tp
print(f"break-even average fraud loss {be_loss:.2f} (assumed 80)")
assert abs(be_loss - 35.0) < 1e-9
# random flagging of the same 20,000 would catch about
rand_tp = flag * fraud_rate
print(f"random 20,000 flags catch about {rand_tp:.0f} frauds; lift of the model = {prec/fraud_rate:.0f}x")
assert rand_tp == 100 and abs(prec / fraud_rate - 35) < 1e-9
# what if the model catches only 2,500 at the same 20,000 flags?
tp2 = 2500; c2 = (frauds - tp2) * loss + flag * review + (flag - tp2) * fp_cost
print(f"if only {tp2:,} caught: cost {c2:,} vs {cost_without:,} without")
assert c2 == 200000 + 40000 + 87500
