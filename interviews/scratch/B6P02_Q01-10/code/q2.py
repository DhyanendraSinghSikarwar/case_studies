# Q2 churn model: top-5% precision 40% -> 31% (illustrative numbers)
import numpy as np
rng = np.random.default_rng(11)

# Identity: precision at top-k = lift x base churn rate
base0, prec0 = 0.10, 0.40
lift0 = prec0 / base0
print(f"launch: base rate {base0:.1%}, top-5% precision {prec0:.0%}, lift {lift0:.1f}x")
assert round(lift0, 2) == 4.0

# Reading A: ranking unchanged (lift stays 4x), the base rate fell
base1 = 0.0775
print(f"A) same lift 4.0x, base rate {base1:.2%} -> precision {lift0*base1:.1%}")
assert round(lift0 * base1, 3) == 0.31
# Reading B: base rate unchanged, ranking got worse
lift1 = 0.31 / base0
print(f"B) same base {base0:.0%}, precision 31% -> lift {lift1:.1f}x (ranking weaker)")
assert round(lift1, 2) == 3.1

# Reading C: the retention team contacted flagged customers and saved some
save_rate = 1 - 0.31 / 0.40
print(f"C) precision falls to 31% if {save_rate:.1%} of would-be churners are saved")
assert round(save_rate, 3) == 0.225

# Noise check: 100,000 customers scored -> 5,000 flagged
n_flag = 5_000
se = (0.31 * 0.69 / n_flag) ** 0.5
print(f"standard error of 31% on {n_flag} flagged: {se*100:.2f} pts; 95% CI [{(0.31-1.96*se)*100:.1f}, {(0.31+1.96*se)*100:.1f}]")
assert 0.006 < se < 0.007 and 0.31 + 1.96 * se < 0.40

# A check that separates A from B without labels shifting: precision among UNTREATED flagged customers
treated = rng.random(n_flag) < 0.6
true_p = np.where(treated, 0.40 * (1 - 0.375), 0.40)          # invented: saves only work in the treated group
churn = rng.random(n_flag) < true_p
p_t, p_u = churn[treated].mean(), churn[~treated].mean()
print(f"treated flagged precision {p_t:.1%}, untreated flagged precision {p_u:.1%}")
assert p_u > p_t + 0.05                  # holdback shows the model ranking is fine; the campaign changes outcomes
mix = 0.6 * 0.40 * (1 - 0.375) + 0.4 * 0.40
print(f"expected blended precision {mix:.1%}")
assert round(mix, 3) == 0.31
