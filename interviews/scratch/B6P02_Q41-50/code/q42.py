# Q42: retrain cadence from decay cost vs retrain cost. Illustrative numbers.
import numpy as np
decay_pp_per_week = 0.3
value_per_pp = 4.0      # Rs lakh per week per percentage point
retrain_cost = 6.0      # Rs lakh per retrain

k = decay_pp_per_week*value_per_pp          # loss rate grows 1.2 lakh/week each week
print(f"loss grows by Rs {k:.1f} lakh per week, per week of age")
assert abs(k - 1.2) < 1e-12

def avg_cost(T):
    # week j of a cycle is j-0.5 weeks old on average, loss = k*(j-0.5); sum_{j=1..T} = k*T^2/2
    weeks = np.arange(1, T+1)
    decay = (k*(weeks-0.5)).sum()
    assert abs(decay - k*T*T/2) < 1e-9
    return (retrain_cost + decay)/T

for T in range(1, 9):
    print(f"retrain every {T} wk: Rs {avg_cost(T):.2f} lakh/week")
best = min(range(1, 13), key=avg_cost)
T_star = (2*retrain_cost/k)**0.5
c_star = (2*retrain_cost*k)**0.5
print(f"continuous optimum T* = sqrt(2R/k) = {T_star:.2f} weeks, cost {c_star:.2f} lakh/week")
assert best == 3 and abs(T_star - 3.162) < 0.001 and abs(c_star - 3.795) < 0.001
assert round(avg_cost(3), 2) == 3.80 and round(avg_cost(4), 2) == 3.90 and round(avg_cost(2), 2) == 4.20

# never retraining: loss grows without bound; after 26 weeks
print(f"never retrain, week 26: loss that week Rs {k*25.5:.1f} lakh; average over 26 wk Rs {k*26/2:.1f} lakh/week")
assert abs(k*26/2 - 15.6) < 1e-9

# assumption breaks: decay is not linear, e.g. a step at week 5 after a shock
def cost_step(T, step_week=5, step_pp=2.0):
    w = np.arange(1, T+1)-0.5
    loss = k*w + np.where(w > step_week, step_pp*value_per_pp, 0.0)
    return (retrain_cost + loss.sum())/T
bestS = min(range(1, 13), key=cost_step)
print("with an extra 2 pp step after week 5, best cadence (whole weeks):", bestS,
      f"cost {cost_step(bestS):.2f}")
# stakes double (e.g. festival season): value_per_pp 8 -> T* shrinks by sqrt(2)
k2 = decay_pp_per_week*8.0
print(f"stakes double: T* = {(2*retrain_cost/k2)**0.5:.2f} weeks")
assert abs((2*retrain_cost/k2)**0.5 - T_star/2**0.5) < 1e-9
# cost rises 4x if retrain costs 24: T* doubles
print(f"retrain cost 4x: T* = {(2*24/k)**0.5:.2f} weeks")
assert abs((2*24/k)**0.5 - 2*T_star) < 1e-9
# slope uncertainty: 0.2 and 0.4 pp per week
for slope in (0.2, 0.4):
    kk = slope*value_per_pp
    print(f"slope {slope} pp/week: T* = {(2*retrain_cost/kk)**0.5:.2f} weeks")
assert abs((2*retrain_cost/(0.2*4))**0.5 - 3.873) < 0.001 and abs((2*retrain_cost/(0.4*4))**0.5 - 2.739) < 0.001
