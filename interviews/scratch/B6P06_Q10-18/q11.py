# Q11: explaining one churn score (illustrative; percentage points)
base = 10.0
contrib = {"feature_1": +6.0, "feature_2": +3.0, "feature_3": -2.0}
score = base + sum(contrib.values())
print("base", base, "sum of contributions", sum(contrib.values()), "score", score)
assert sum(contrib.values()) == 7.0 and score == 17.0
# additivity check: dropping the largest contributor
print("score if feature_1 contribution were zero:", score - contrib["feature_1"])
assert score - contrib["feature_1"] == 11.0
# relative framing
print("risk ratio vs base:", round(score / base, 2))
assert round(score / base, 2) == 1.7
# What additivity does NOT say: removing feature_1 from the real model need not give 11.
# Tiny interaction example: p = 0.10 + 0.05*a + 0.05*b + 0.20*a*b with a=b=1 -> 0.40.
# Shapley split of the interaction is even, so a and b each get 0.05 + 0.10 = 0.15, base 0.10.
def f(a, b): return 0.10 + 0.05 * a + 0.05 * b + 0.20 * a * b
phi_a = 0.5 * ((f(1, 0) - f(0, 0)) + (f(1, 1) - f(0, 1)))
phi_b = 0.5 * ((f(0, 1) - f(0, 0)) + (f(1, 1) - f(1, 0)))
print("Shapley a", round(phi_a, 3), "b", round(phi_b, 3), "sum + base", round(f(0, 0) + phi_a + phi_b, 3))
assert abs(f(0, 0) + phi_a + phi_b - f(1, 1)) < 1e-12
print("but setting a to 0 changes p by", round(f(1, 1) - f(0, 1), 3), "not", round(phi_a, 3))
assert abs((f(1, 1) - f(0, 1)) - 0.25) < 1e-12 and abs(phi_a - 0.15) < 1e-12
