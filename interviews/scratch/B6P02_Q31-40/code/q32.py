# Q32: is 91% -> 86% on 400 tickets a real decline? (numbers from the prompt, rest illustrative)
import math
import numpy as np

def phi_upper(z): return 0.5 * math.erfc(z / math.sqrt(2))     # P(Z > z)

a_ok, b_ok, n = 364, 344, 400
pa, pb = a_ok / n, b_ok / n
assert (pa, pb) == (0.91, 0.86)
pool = (a_ok + b_ok) / (2 * n)
se_pool = math.sqrt(pool * (1 - pool) * (2 / n))
z = (pa - pb) / se_pool
p_two = 2 * phi_upper(z)
se_diff = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
lo, hi = (pa - pb) - 1.96 * se_diff, (pa - pb) + 1.96 * se_diff
print(f"drop {pa - pb:.3f}  z {z:.2f}  two-sided p {p_two:.4f}  95% CI for the drop [{lo:.3f}, {hi:.3f}]")
assert round(z, 2) == 2.22 and 0.02 < p_two < 0.035 and 0.004 < lo < 0.008 and 0.09 < hi < 0.10

# Power: tickets per week needed to detect a 5-point drop from 91% (80% power, 5% two-sided)
za, zb = 1.96, 0.8416
need = (za + zb) ** 2 * (pa * (1 - pa) + pb * (1 - pb)) / (pa - pb) ** 2
print(f"tickets per week for 80% power at a 5-point drop: {need:.0f}")
assert 600 < need < 700

# Weekly checking: if the true accuracy never changes (89%), how often does a week
# look 'significantly lower' than the previous week at the 5% one-sided level?
rng = np.random.default_rng(32)
weeks = 20_000
x = rng.binomial(n, 0.89, size=weeks + 1)
p = x / n
z_w = (p[:-1] - p[1:]) / np.sqrt(2 * 0.89 * 0.11 / n)
false_alarm = (z_w > 1.645).mean()
print(f"false 'decline' weeks when nothing changed: {false_alarm:.3f}  (about 1 in {1 / false_alarm:.0f} weeks)")
assert 0.03 < false_alarm < 0.07

# Mix effect: launch added a new ticket type the model never saw. Same model, same skill on old types.
before = {"old types": (400, 364)}                    # (tickets, correct)
after = {"old types": (300, 276), "new type": (100, 68)}
acc = lambda d: sum(c for _, c in d.values()) / sum(t for t, _ in d.values())
print(f"before {acc(before):.2%}  after {acc(after):.2%}")
print(f"old types: {364 / 400:.1%} -> {276 / 300:.1%}   new type: {68 / 100:.0%}   new-type share {100 / 400:.0%}")
assert acc(before) == 0.91 and acc(after) == 0.86
assert 276 / 300 == 0.92 and 68 / 100 == 0.68
# exact decomposition of the 5-point drop (reference = old accuracy 91%)
new_part = 0.25 * (0.68 - 0.91)      # new ticket type
old_part = 0.75 * (0.92 - 0.91)      # old ticket types
print(f"new type {new_part:+.4f}  old types {old_part:+.4f}  total {new_part + old_part:+.4f}")
assert abs(new_part + old_part - (0.86 - 0.91)) < 1e-12
assert abs(new_part) > 5 * abs(old_part)
