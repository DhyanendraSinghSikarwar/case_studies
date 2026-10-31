gain, loss = 150.0, 600.0
be = gain / (gain + loss)
print(f"break-even PD = {gain}/({gain}+{loss}) = {be:.0%}")
assert abs(be - 0.20) < 1e-12
def ev(pd): return (1 - pd) * gain - pd * loss
for pd in (0.05, 0.20, 0.30):
    print(f"PD {pd:.0%}: expected profit per loan {ev(pd):+.2f}")
assert abs(ev(0.05) - 112.5) < 1e-9 and abs(ev(0.20)) < 1e-9 and abs(ev(0.30) + 75) < 1e-9
# calibration error: model says 15%, truth is 1.5x higher
pred, true = 0.15, 0.225
print(f"model says {pred:.0%} -> approve, expected {ev(pred):+.2f}; true {true:.1%} gives {ev(true):+.2f}")
assert ev(pred) > 0 > ev(true)
# portfolio view: PD uniformly spread 0-40%, cut at 20% vs cut at 10%
import numpy as np
pds = np.linspace(0, 0.4, 4001)
prof = lambda cut: sum(ev(p) for p in pds if p <= cut)
print(f"per 4,001 applicants (PD 0-40%): total profit cut 20% {prof(0.20):,.0f}; cut 10% {prof(0.10):,.0f}; cut 30% {prof(0.30):,.0f}")
assert prof(0.20) > prof(0.10) and prof(0.20) > prof(0.30)
# loss given default larger: 900 instead of 600 moves the cut-off
print(f"if loss is 900, break-even PD = {gain/(gain+900):.1%}")
assert abs(gain/(gain+900) - 0.142857) < 1e-5
