# Q48: AI summary box. Click-through -18%, satisfaction up. Illustrative numbers only.
import numpy as np
rng = np.random.default_rng(48)

N = 100_000                                   # sessions per arm
ctr_c, ctr_t = 0.200, 0.164                   # share of sessions with an article click
assert round(ctr_t / ctr_c - 1, 3) == -0.18
click_c, click_t = int(N * ctr_c), int(N * ctr_t)
noclick_c, noclick_t = N - click_c, N - click_t
print("click sessions:", click_c, "->", click_t, "| no-click sessions:", noclick_c, "->", noclick_t)

# survey on no-click sessions (n=2000 per arm, true satisfied rates 55% vs 70%)
sat_c = rng.binomial(2000, 0.55) / 2000
sat_t = rng.binomial(2000, 0.70) / 2000
se = np.sqrt(sat_c*(1-sat_c)/2000 + sat_t*(1-sat_t)/2000)
diff = sat_t - sat_c
print(f"no-click satisfied: {sat_c:.3f} -> {sat_t:.3f}, diff {diff:+.3f}, 95% CI +/- {1.96*se:.3f}")
assert diff - 1.96*se > 0.10

# user-side metric: successful sessions = clicked and stayed (assume 85% of clicks are good) + satisfied no-click
good_click = 0.85
succ_c = (click_c*good_click + noclick_c*0.55) / N
succ_t = (click_t*good_click + noclick_t*0.70) / N
print(f"successful-session rate: {succ_c:.3f} -> {succ_t:.3f}")
assert round(succ_c, 3) == 0.610 and round(succ_t, 3) == 0.725      # 0.17+0.44 ; 0.1394+0.5852 = 0.7246 -> 0.725

# publisher side: value per 100k sessions at an assumed Rs 4 of publisher revenue per click session
rev_c, rev_t = click_c * 4, click_t * 4
print(f"publisher revenue per 100k sessions (Rs): {rev_c} -> {rev_t} ({rev_t/rev_c-1:+.0%})")
assert rev_c == 80_000 and rev_t == 65_600 and round(rev_t/rev_c - 1, 2) == -0.18

# guardrail rule: ship only if publisher click share loss <= 10% unless source-link clicks recover it
loss = 1 - click_t / click_c
guard = 0.10
print(f"publisher click loss {loss:.0%} vs guardrail {guard:.0%} ->", "BREACH, fix source links" if loss > guard else "ok")
assert loss > guard
# what source-link prominence must recover to get back inside the guardrail
need = click_c * (1 - guard) - click_t
print("extra click sessions per 100k needed to meet the guardrail:", int(need))
assert int(need) == 1600
