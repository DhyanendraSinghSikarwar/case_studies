import numpy as np
# Part A: prompt arithmetic (illustrative; 2.0% new-listing rate is a projection)
imps = 10_000_000
expl = 0.05 * imps
orders_expl = expl * 0.02
orders_normal_same_imps = expl * 0.03
lost = orders_normal_same_imps - orders_expl
base_orders = imps * 0.03                    # if every impression converted at 3.0%
print(f"exploration impressions {expl:,.0f}; orders {orders_expl:,.0f} instead of {orders_normal_same_imps:,.0f}; lost {lost:,.0f} = {lost/base_orders:.2%} of {base_orders:,.0f}")
# the 2% share new sellers already get: if the 5% includes it, only 3 points are extra
extra = (0.05 - 0.02) * imps
lost_net = extra * (0.03 - 0.02)
base2 = 0.98 * imps * 0.03 + 0.02 * imps * 0.02
print(f"if 5% includes today's 2%: extra exploration {extra:,.0f} impressions, lost {lost_net:,.0f} = {lost_net/base2:.2%} of {base2:,.0f}")
for r in (0.015, 0.02, 0.025):
    print(f"  if new listings convert at {r:.1%}: lost {expl*(0.03-r):,.0f} orders/day ({expl*(0.03-r)/base_orders:.2%})")
# impressions to tell a 2.0% listing from the 3% benchmark (variance taken at 2.5%) (one-sample, 5% two-sided, 80% power)
p = 0.025; delta = 0.01
n_one = (1.96 + 0.84) ** 2 * p * (1 - p) / delta ** 2
print(f"impressions per listing to separate 2.0% from 3.0%: about {n_one:,.0f}; the budget covers {expl/n_one:,.0f} listings a day at that depth")
assert expl == 500_000 and round(orders_expl) == 10_000 and round(lost) == 5_000 and round(base_orders) == 300_000
assert round(lost / base_orders, 4) == 0.0167
assert extra == 300_000 and round(lost_net) == 3_000 and round(base2) == 298_000 and round(lost_net / base2, 4) == 0.0101
assert round(expl * 0.015) == 7_500 and round(n_one) == 1_911 and round(expl / n_one) == 262

# Part B: uniform exploration versus Thompson sampling over 2,000 new listings (invented conversion rates)
rng = np.random.default_rng(5)
L, budget, rounds = 2_000, 500_000, 20
true = rng.beta(2, 98, L)                    # mean about 2%
def run(adaptive):
    a = np.ones(L); b = np.ones(L); orders = 0
    per_round = budget // rounds
    for _ in range(rounds):
        if adaptive:
            draw = rng.beta(a, b)
            pick = rng.choice(L, size=per_round, p=draw / draw.sum())   # probability matching on a posterior draw
        else:
            pick = rng.integers(0, L, per_round)
        shows = np.bincount(pick, minlength=L)
        conv = rng.binomial(shows, true)
        a += conv; b += shows - conv; orders += conv.sum()
    top = np.argsort(-(a / (a + b)))[:200]
    return orders, true[top].mean(), true[np.argsort(-true)[:200]].mean()
o_u, q_u, best = run(False); o_t, q_t, _ = run(True)
print(f"uniform: {o_u:,} orders, mean true rate of picked top 200 {q_u:.4f}; Thompson-style: {o_t:,} orders, {q_t:.4f}; oracle top 200 {best:.4f}")
assert o_t > o_u and q_t > q_u
assert round(o_t / o_u - 1, 2) == 0.26
