cust, lift_pp, value = 1_000_000, 0.4, 20
extra = cust * lift_pp / 100
gain = extra * value
print(f"extra conversions {extra:,.0f}, gain {gain:,.0f}")
assert extra == 4000 and gain == 80_000
# break-even: how likely/large must the downside be to cancel the gain? (loss figure is illustrative)
for loss in (500_000, 2_000_000, 10_000_000):
    print(f"  if loss on a breach is {loss:,}: break-even probability {gain/loss:.1%}")
assert abs(80_000/2_000_000 - 0.04) < 1e-12
# uncertainty in the lift: illustrative test with 100,000 per arm, base conversion 5%
import math
se = math.sqrt(2*0.05*0.95/100_000)
lo, hi = lift_pp/100 - 1.96*se, lift_pp/100 + 1.96*se
print(f"lift 0.40pp, 95% CI {lo*100:.2f}pp to {hi*100:.2f}pp -> gain {lo*cust*value:,.0f} to {hi*cust*value:,.0f}")
assert 0.20 < lo*100 < 0.22 and 0.58 < hi*100 < 0.60
# legal options (illustrative rates)
optin = 0.25
consent_gain = cust*optin*lift_pp/100*value
coarse_gain = 0.5*gain
print(f"opt-in route at {optin:.0%} consent: {consent_gain:,.0f}; coarse region-level feature at half the lift: {coarse_gain:,.0f}")
assert consent_gain == 20_000 and coarse_gain == 40_000
