# Q8: notification experiment (illustrative numbers)
import math

n = 200_000  # users per arm
p_c, p_t = 0.012, 0.015
pool = (p_c + p_t) / 2
se = math.sqrt(pool * (1 - pool) * 2 / n)
z = (p_t - p_c) / se
diff = p_t - p_c
ci = (diff - 1.96 * se, diff + 1.96 * se)
print(f"uninstalls 30d: {p_c:.1%} vs {p_t:.1%}; diff {diff*100:.2f}pp CI [{ci[0]*100:.2f}, {ci[1]*100:.2f}] z={z:.1f}")
assert z > 4 and ci[0] > 0
extra = diff * n
print(f"extra uninstalls per arm of {n:,}: {extra:.0f}")
assert round(extra) == 600

# Does a 2% DAU lift survive the uninstalls? Monthly uninstall hazard as measured, lift held constant.
lift = 0.02
print("month  DAU index (treatment / control)")
cross = None
for m in range(1, 13):
    idx = (1 + lift) * ((1 - p_t) / (1 - p_c)) ** m
    print(f"{m:5d}  {idx:.4f}")
    if cross is None and idx < 1:
        cross = m
print(f"crossover month: {cross}")
assert cross == 7
print("Assumes the lift stays 2% and the uninstall rate repeats monthly: both are things to measure.")
