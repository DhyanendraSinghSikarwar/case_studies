import numpy as np
# Part A: arithmetic at elasticity -1.2 for a 5% relative price rise (illustrative price 10, cost 6)
e = -1.2
units_f = 1.05 ** e
print(f"units factor {units_f:.4f} ({units_f-1:+.2%}); linear rule of thumb gives {e*5:+.1f}%")
assert round(units_f - 1, 4) == -0.0569
rev_f = 1.05 * units_f
print(f"revenue factor {rev_f:.4f} ({rev_f-1:+.2%})")
assert round(rev_f - 1, 4) == -0.0097
p0, c = 10.0, 6.0
prof0 = (p0 - c) * 1.0; prof1 = (p0 * 1.05 - c) * units_f
print(f"gross profit per base unit {prof0:.2f} -> {prof1:.3f} ({prof1/prof0-1:+.1%})")
assert round(prof1 / prof0 - 1, 3) == 0.061
# Part B: simulate why pooled OLS can show +0.4, and why fixed effects may still be biased.
rng = np.random.default_rng(11)
S, W = 50, 100
true_e = -1.2
a_s = rng.normal(0, 0.5, S)[:, None]            # store size effect on log units
w_t = rng.normal(0, 0.2, W)[None, :]            # chain-wide weekly demand
u = rng.normal(0, 0.15, (S, W))                 # store-week demand shock the manager anticipates
b_s = 0.6 * a_s                                  # big stores charge more
g_t = 0.5 * w_t                                  # prices follow the season
cost_shock = rng.normal(0, 0.05, (S, W))        # supplier cost moves, unrelated to demand (an instrument)
logp = 2.0 + b_s + g_t + 0.8 * u + cost_shock + rng.normal(0, 0.02, (S, W))
logq = 5.0 + a_s + w_t + true_e * logp + u + rng.normal(0, 0.05, (S, W))
def ols(y, X):
    X = np.column_stack([np.ones(len(y)), X]); return np.linalg.lstsq(X, y, rcond=None)[0]
y, x = logq.ravel(), logp.ravel()
pooled = ols(y, x)[1]
# two-way demeaning = store and week fixed effects
def tw(m): return m - m.mean(1, keepdims=True) - m.mean(0, keepdims=True) + m.mean()
fe = (tw(logp).ravel() @ tw(logq).ravel()) / (tw(logp).ravel() @ tw(logp).ravel())
# IV with the cost shock inside the FE model
z = tw(cost_shock).ravel()
iv = (z @ tw(logq).ravel()) / (z @ tw(logp).ravel())
print(f"pooled {pooled:+.2f} | store+week FE {fe:+.2f} | FE + cost-shock IV {iv:+.2f} | truth {true_e:+.2f}")
assert pooled > 0 and fe > true_e and abs(iv - true_e) < 0.15
assert fe < 0
