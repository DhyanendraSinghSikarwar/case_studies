# Q49: paired sensitivity comparison (prompt numbers + INVENTED discordant counts)
import math
n = 400
old_tp, new_tp = round(0.82 * n), round(0.80 * n)
print("true positives old/new:", old_tp, new_tp, " difference:", new_tp - old_tp)
assert (old_tp, new_tp) == (328, 320)
se_new_alone = math.sqrt(0.8 * 0.2 / n)
print("SE of the new sensitivity alone:", se_new_alone)
assert abs(se_new_alone - 0.02) < 1e-12
# Unpaired (wrong for a paired design): SE of difference if the two were independent
se_unpaired = math.sqrt(0.82 * 0.18 / n + 0.8 * 0.2 / n)
print("unpaired SE of difference (not appropriate):", round(se_unpaired, 4))

# Paired: c = positives only the new model catches, b = only the old model catches; c - b = -8
margin = 0.03   # illustrative non-inferiority margin, absolute sensitivity points; clinicians must set it
print("margin:", margin)
for b, c in [(12, 4), (20, 12), (40, 32), (60, 52)]:
    assert c - b == -8
    d = (c - b) / n
    se = math.sqrt(b + c - (c - b) ** 2 / n) / n          # paired SE for a difference in proportions
    lo, hi = d - 1.96 * se, d + 1.96 * se
    lo1 = d - 1.645 * se                                      # one-sided 95% lower bound for non-inferiority
    print(f"discordant b={b:2d} c={c:2d}: diff {d:+.3f} SE {se:.4f} 95% CI [{lo:+.3f}, {hi:+.3f}] one-sided lower {lo1:+.3f} non-inferior at 0.03? {lo1 > -margin}; at 0.05? {lo1 > -0.05}")
# with b=20, c=12 (invented): lower bound below -0.03 -> cannot claim non-inferiority
b, c = 20, 12
se = math.sqrt(b + c - (c - b) ** 2 / n) / n
assert (-8 / n) - 1.645 * se < -margin
# sample needed: positives for a non-inferiority test if the true difference is 0, discordant rate 8% (invented)
disc = 0.08
n_pos = ((1.645 + 0.8416) ** 2) * disc / (margin ** 2)       # one-sided alpha 0.05, 80% power, true diff 0
print("positives needed (true diff 0, discordance 8%, margin 3 pts):", math.ceil(n_pos))
assert math.ceil(n_pos) == 550
