# Q27 fraud bands (illustrative numbers, one day)
total = 1_000_000
band = {"block": (2_000, 1_200), "step": (18_000, 600), "pass": (980_000, 200)}
assert sum(n for n, _ in band.values()) == total
fraud = sum(f for _, f in band.values())
assert fraud == 2_000
stop_block = band["block"][1]
stop_step = 0.8 * band["step"][1]
stopped = stop_block + stop_step
assert stop_step == 480 and stopped == 1_680
through = fraud - stopped
assert through == 320
# of which: 120 pass step-up, 200 in pass band
assert band["step"][1] - stop_step == 120
gen = {k: n - f for k, (n, f) in band.items()}
assert gen == {"block": 800, "step": 17_400, "pass": 979_800}
lost_step = 0.10 * gen["step"]
assert lost_step == 1_740
print(f"fraud total {fraud}, stopped {stopped:.0f} ({stopped/fraud:.0%}), through {through:.0f}")
print(f"genuine blocked {gen['block']}, genuine lost at step-up {lost_step:.0f}")
for k, (n, f) in band.items():
    print(f"{k:5} flagged {n:>7} fraud {f:>5} fraud rate {f/n:.2%}")
assert round(1_200/2_000, 2) == 0.60 and round(600/18_000, 4) == 0.0333

# Choosing the edges: expected cost per 1,000 in a band, invented costs
loss_per_fraud = 2_500      # average loss if fraud gets through
block_fp = 150              # cost of a wrongly blocked genuine customer (care, lost sale, churn)
step_fp = 0.10 * 400        # 10% abandon x 400 lost margin (invented), per genuine customer stepped up
step_cost = 15              # friction cost per step-up customer
def block_gain(p):          # benefit minus cost of blocking one txn with fraud probability p
    return p * loss_per_fraud - (1 - p) * block_fp
def step_gain(p):
    return p * 0.8 * loss_per_fraud - (1 - p) * step_fp - step_cost
print(f"block band (p=60%): gain per txn {block_gain(0.6):,.0f}")
print(f"step band (p=3.33%): gain per txn {step_gain(600/18_000):,.1f}")
# break-even fraud probabilities
p_block = block_fp / (loss_per_fraud + block_fp)
p_step = (step_fp + step_cost) / (0.8 * loss_per_fraud + step_fp)
print(f"break-even p: block above {p_block:.1%}, step-up above {p_step:.2%}")
assert abs(p_block - 0.0566) < 1e-3 and abs(p_step - 0.0269) < 1e-3
assert block_gain(0.6) > 0 and step_gain(600/18_000) > 0
