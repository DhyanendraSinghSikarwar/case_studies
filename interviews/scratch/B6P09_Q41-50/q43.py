# Q43: recommender, CTR up, GMV down. Prompt numbers + INVENTED sample sizes / variance (the prompt gives none).
import math
ctr0, ctr1 = 0.0400, 0.0424
print("CTR abs diff pts:", round((ctr1 - ctr0) * 100, 2), " relative:", round(ctr1 / ctr0 - 1, 4))
assert round((ctr1 - ctr0) * 100, 2) == 0.24 and round(ctr1 / ctr0 - 1, 4) == 0.06
g0, g1 = 500.0, 497.5
print("GMV/user rel change:", round(g1 / g0 - 1, 4))
assert round(g1 / g0 - 1, 4) == -0.005
lt0, lt1 = 0.30, 0.18
print("long-tail share: abs pts", round((lt1 - lt0) * 100), " relative", round(lt1 / lt0 - 1, 2))
assert round((lt1 - lt0) * 100) == -12 and round(lt1 / lt0 - 1, 2) == -0.40

# invented: 2,000,000 impressions per arm
imp = 2_000_000
se_ctr = math.sqrt(ctr0 * (1 - ctr0) / imp + ctr1 * (1 - ctr1) / imp)
z_ctr = (ctr1 - ctr0) / se_ctr
print("CTR z (2M impressions/arm, invented):", round(z_ctr, 1))
assert z_ctr > 10

# invented: 200,000 users per arm, per-user GMV sd 2,000 (heavy-tailed)
users, sd = 200_000, 2_000.0
se_g = sd * math.sqrt(2 / users)
d = g1 - g0
lo, hi = d - 1.96 * se_g, d + 1.96 * se_g
print(f"GMV diff {d} se {se_g:.2f} z {d/se_g:.2f} 95% CI [{lo:.1f}, {hi:.1f}] = [{lo/g0:.2%}, {hi/g0:.2%}]")
assert abs(d / se_g) < 1.96            # with these inputs the GMV drop is not distinguishable from zero
assert lo / g0 < -0.025                # but a 2.5% loss is not ruled out

# users per arm needed to detect a 0.5% GMV change (80% power, 5% two-sided)
delta = 0.005 * g0
n_needed = 2 * ((1.96 + 0.8416) ** 2) * sd ** 2 / delta ** 2
print("users per arm to detect 0.5% GMV change:", round(n_needed))
assert 9_900_000 < n_needed < 10_100_000
