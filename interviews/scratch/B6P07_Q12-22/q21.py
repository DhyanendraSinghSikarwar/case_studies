import math
calls = 5_000_000
big, small, one_off = 0.004, 0.0005, 13_000
mb, ms = calls * big, calls * small
saving = mb - ms
payback = one_off / saving
print(f"monthly: large {mb:,.0f}, small {ms:,.0f}, saving {saving:,.0f}; payback {payback:.2f} months (~{payback*30:.0f} days)")
assert (mb, ms, saving) == (20_000, 2_500, 17_500) and round(payback, 2) == 0.74
extra_err = calls * 0.02
be = saving / extra_err
print(f"2 points = {extra_err:,.0f} extra errors a month; break-even cost per extra error = {be:.3f} = {be/big:.2f}x the large call")
assert round(extra_err) == 100_000 and round(be, 3) == 0.175 and round(be / big, 2) == 43.75
# Test-set noise: assume large model 92% and small 90% on the same 500 tickets (invented).
n = 500
p1, p2 = 0.92, 0.90
se = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
print(f"unpaired SE {se*100:.2f} pts; CI of the -2 pt gap {(-0.02-1.96*se)*100:.1f} to {(-0.02+1.96*se)*100:.1f} pts")
assert round(se * 100, 2) == 1.81 and round((-0.02 - 1.96 * se) * 100, 1) == -5.5 and round((-0.02 + 1.96 * se) * 100, 1) == 1.5
# Cascade: small model answers, a fraction escalates to the large model.
for esc in (0.0, 0.2, 0.4):
    c = calls * small + esc * calls * big
    print(f"escalate {esc:.0%}: monthly {c:,.0f}, saving {mb-c:,.0f}")
assert calls * small + 0.2 * calls * big == 6_500
