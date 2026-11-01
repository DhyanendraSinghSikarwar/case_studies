# Q31: batching two orders per courier (illustrative)
single, batch = 3.50, 2.40
late0, late1, refund = 0.08, 0.14, 4.00
saving = single - batch
extra_late_cost = (late1 - late0) * refund
net = saving - extra_late_cost
print(f"courier saving {saving:.2f}; extra expected refund {extra_late_cost:.2f}; net saving per delivery {net:.2f}")
assert abs(saving - 1.10) < 1e-9 and abs(extra_late_cost - 0.24) < 1e-9 and abs(net - 0.86) < 1e-9
assert abs((late1 - late0) - 0.06) < 1e-12

# totals per delivery (courier + expected refunds)
tot0 = single + late0 * refund
tot1 = batch + late1 * refund
print(f"total cost per delivery: single {tot0:.2f}; batched {tot1:.2f}; difference {tot0-tot1:.2f}")
assert abs(tot0 - 3.82) < 1e-9 and abs(tot1 - 2.96) < 1e-9

# break-even late rate for batching
be_late = (single + late0 * refund - batch) / refund
print(f"break-even late rate for batching {be_late:.1%} ({(be_late-late0)*100:.1f} points above 8%)")
assert abs(be_late - 0.355) < 1e-9

# if each late order really costs more (refund + goodwill + lost repeat), break-even refund at 14% late
be_refund = saving / (late1 - late0)
print(f"break-even cost per late delivery at 14% vs 8% late: {be_refund:.2f}")
assert abs(be_refund - 18.3333) < 1e-3
# batching only half of orders: saving scales with batched share
for share in (1.0, 0.5, 0.25):
    print(f"  batch share {share:.0%}: net saving per delivery overall {share*net:.3f}")
assert abs(0.5 * net - 0.43) < 1e-9
