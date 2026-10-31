# Q11: both segments up, overall down (illustrative sessions)
before = {"mobile": (5_000, 0.020), "desktop": (5_000, 0.060)}
after  = {"mobile": (6_000, 0.022), "desktop": (4_000, 0.062)}

def overall(d):
    s = sum(v[0] for v in d.values()); c = sum(v[0] * v[1] for v in d.values())
    return c / s
b, a = overall(before), overall(after)
print(f"overall {b:.1%} -> {a:.1%}")
assert round(b, 4) == 0.04 and round(a, 4) == 0.038
for k in before:
    print(f"{k:8} share {before[k][0]/10_000:.0%} -> {after[k][0]/10_000:.0%}, conv {before[k][1]:.1%} -> {after[k][1]:.1%}")

# split: within-segment effect at old mix, mix effect at new rates
w0 = {k: v[0] / 10_000 for k, v in before.items()}
w1 = {k: v[0] / 10_000 for k, v in after.items()}
within = sum(w0[k] * (after[k][1] - before[k][1]) for k in w0)
mix = sum((w1[k] - w0[k]) * after[k][1] for k in w0)
print(f"within-segment effect {within*100:+.2f}pp, mix effect {mix*100:+.2f}pp, total {(within+mix)*100:+.2f}pp")
assert round(within, 4) == 0.002 and round(mix, 4) == -0.004
assert abs(within + mix - (a - b)) < 1e-12

# what mobile share is needed for overall 3.8% with these rates?
m = (0.062 - 0.038) / (0.062 - 0.022)
print(f"mobile share that gives 3.8%: {m:.0%}")
assert round(m, 2) == 0.60
