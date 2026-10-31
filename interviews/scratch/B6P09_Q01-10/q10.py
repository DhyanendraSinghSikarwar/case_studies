import numpy as np
# Part A: prompt arithmetic (illustrative). Called 3,000 -> 40% paid; random holdout of 300 not called -> 35% paid.
nc, pc, nh, ph = 3_000, 0.40, 300, 0.35
paid_called = nc * pc
paid_hold = nh * ph
uplift = pc - ph
incr = nc * uplift
value, cost = 8_000, 150
net = incr * value - nc * cost
be_uplift = cost / value
se = (pc * (1 - pc) / nc + ph * (1 - ph) / nh) ** 0.5
lo, hi = uplift - 1.96 * se, uplift + 1.96 * se
print(f"paid called {paid_called:.0f}, paid holdout {paid_hold:.0f}; uplift {uplift:.1%}; incremental payments {incr:.0f}")
print(f"value {incr*value:,.0f} - call cost {nc*cost:,} = net {net:,.0f}; break-even uplift {be_uplift:.3%}")
print(f"SE of the 5-point gap {se*100:.2f} points; 95% interval {lo*100:.1f} to {hi*100:.1f} points -> incremental payments {nc*lo:.0f} to {nc*hi:.0f}, net {nc*lo*value-nc*cost:,.0f} to {nc*hi*value-nc*cost:,.0f}")
learn_cost = nh * uplift * value - nh * cost   # expected value given up by not calling the 300 (value of their uplift minus calls saved)
print(f"expected cost of keeping 300 uncalled: {learn_cost:,.0f}")
assert paid_called == 1200 and paid_hold == 105 and round(uplift, 6) == 0.05 and round(incr) == 150
assert round(incr * value) == 1_200_000 and nc * cost == 450_000 and round(net) == 750_000 and round(be_uplift, 5) == 0.01875
assert round(se * 100, 2) == 2.90 and lo < 0 < hi
assert round(nc * lo) == -20 and round(nc * hi) == 320 and round(learn_cost) == 75_000

# Part B: rank by P(pay) versus rank by uplift on synthetic accounts (seeded). Random calls on half the accounts give the training data.
rng = np.random.default_rng(21)
N, K = 10_000, 3_000
x1 = rng.random(N)                              # 'ability to pay' (drives baseline payment)
x2 = rng.random(N)                              # 'persuadability' (drives the effect of a call)
base_p = 0.05 + 0.75 * x1 ** 2                 # sure-things at high x1
eff = 0.30 * np.exp(-6 * (x1 - 0.35) ** 2) * x2  # calls matter most at middling x1 and high x2 (invented)
p_call = np.clip(base_p + eff, 0, 0.97)
# training data: 200,000 randomised past accounts, called with probability 0.5
M = 200_000
t1, t2 = rng.random(M), rng.random(M)
tb = 0.05 + 0.75 * t1 ** 2; te = 0.30 * np.exp(-6 * (t1 - 0.35) ** 2) * t2
tr = rng.random(M) < 0.5
pay = rng.random(M) < np.clip(tb + te * tr, 0, 0.97)
g = 10
cell = (np.minimum((t1 * g).astype(int), g - 1)) * g + np.minimum((t2 * g).astype(int), g - 1)
est_up = np.zeros(g * g); est_p = np.zeros(g * g)
for c in range(g * g):
    m = cell == c
    est_up[c] = pay[m & tr].mean() - pay[m & ~tr].mean()          # T-learner by cell
    est_p[c] = pay[m & tr].mean()                                 # what a P(pay | called) model learns
acell = (np.minimum((x1 * g).astype(int), g - 1)) * g + np.minimum((x2 * g).astype(int), g - 1)
def evaluate(score):
    top = np.argsort(-score)[:K]
    gain = (p_call[top] - base_p[top]).sum()                      # expected incremental payments (true effect)
    return gain, gain * value - K * cost
g_p, n_p = evaluate(est_p[acell]); g_u, n_u = evaluate(est_up[acell]); g_o, n_o = evaluate(eff)
print(f"call the top 3,000 ranked by P(pay): {g_p:.0f} incremental payments, net {n_p:,.0f}")
print(f"call the top 3,000 ranked by estimated uplift: {g_u:.0f} incremental payments, net {n_u:,.0f} (oracle {g_o:.0f})")
assert g_u > g_p * 1.3 and n_u > n_p
assert g_u > 0.85 * g_o
