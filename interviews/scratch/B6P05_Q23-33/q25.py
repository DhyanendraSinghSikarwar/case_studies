# Q25: recommender, CTR lift vs money (illustrative)
ctr0, ctr1 = 0.05, 0.08
print(f"CTR {ctr0:.0%} -> {ctr1:.0%}: +{(ctr1-ctr0)*100:.0f} points absolute, +{(ctr1/ctr0-1)*100:.0f}% relative")
assert abs((ctr1 - ctr0) - 0.03) < 1e-12 and abs(ctr1 / ctr0 - 1.6) < 1e-12

users, rpu_m, rpu_p, margin, cost = 2_000_000, 40.0, 39.0, 0.30, 250_000
rel = rpu_m / rpu_p - 1
inc_rev = (rpu_m - rpu_p) * users
inc_margin = inc_rev * margin
net = inc_margin - cost
print(f"revenue per user +{rpu_m-rpu_p:.1f} = +{rel*100:.2f}% relative to 39.0 (the prompt's 2.5% is 1/40; against 39.0 it is 2.56%)")
print(f"incremental revenue {inc_rev:,.0f}; incremental margin {inc_margin:,.0f}; cost {cost:,}; net value {net:,.0f}")
assert abs(rel - 0.02564) < 1e-4 and inc_rev == 2_000_000 and inc_margin == 600_000 and net == 350_000

# break-even revenue lift per user, and noise check with an ASSUMED standard deviation
be_rpu = cost / (users * margin)
print(f"break-even lift in revenue per user = {be_rpu:.3f} ({be_rpu/rpu_p*100:.2f}% of 39.0)")
assert abs(be_rpu - 0.41667) < 1e-4
import math
for sd in (30, 60, 120):
    n_arm = users / 2           # if the 2,000,000 users were split evenly between the two arms
    se = sd * math.sqrt(2 / n_arm)
    print(f"assumed sd {sd}: SE of the difference {se:.3f}; observed 1.0 is {1.0/se:.1f} SEs; break-even 0.417 is {(1.0-be_rpu)/se:.1f} SEs below it")
assert 1.0 / (60 * math.sqrt(2 / 1_000_000)) > 10

# the click lift is 60% relative; the revenue lift is 2.56% relative
print(f"revenue lift / click lift (both relative) = {rel/(ctr1/ctr0-1):.3f}")
assert abs(rel / 0.6 - 0.0427) < 1e-3
