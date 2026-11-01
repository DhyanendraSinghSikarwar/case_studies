import numpy as np
# SYNTHETIC: per-token accuracy rises smoothly with log model size; exact match needs k tokens all right.
sizes = np.logspace(7, 11, 9)                       # 1e7 ... 1e11 "parameters"
p = 1 / (1 + np.exp(-(np.log10(sizes) - 8.5) * 1.2))   # smooth per-token accuracy (logistic in log N), assumed
k = 10
em = p ** k
print("params   per-token acc   exact-match(k=10)")
for n, a, e in zip(sizes, p, em):
    print(f"{n:8.0e}   {a:6.3f}          {e:6.3f}")
# noise: with a test set of 100 items, standard error of an accuracy near 0.05 is ~0.022
for n_items in (100, 1000):
    se = (0.05 * 0.95 / n_items) ** 0.5
    print(f"test set {n_items}: std error at acc=0.05 is {se:.3f}")
