import numpy as np
from scipy.optimize import linear_sum_assignment
rng = np.random.default_rng(1)
orders = rng.uniform(0, 5, (4, 2)); riders = rng.uniform(0, 5, (4, 2))   # km coordinates
cost = np.linalg.norm(orders[:, None] - riders[None], axis=2)            # pickup distance
r, c = linear_sum_assignment(cost)
greedy = 0; free = set(range(4))
for i in range(4):                                                        # greedy: each order grabs nearest free rider
    j = min(free, key=lambda k: cost[i, k]); greedy += cost[i, j]; free.remove(j)
print("optimal total km:", round(cost[r, c].sum(), 2), "| greedy total km:", round(greedy, 2))
