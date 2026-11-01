# Q41: loss-filter cleaning and a small dialect group. Illustrative numbers.
import numpy as np

# --- prompt arithmetic ---
N, drop, G, g_drop = 60_000, 3_000, 2_400, 900
assert drop == int(0.05 * N) and G == int(0.04 * N)
print(f"group rows dropped: {g_drop}/{G} = {g_drop/G:.1%}")
print(f"other rows dropped: {drop-g_drop}/{N-G} = {(drop-g_drop)/(N-G):.2%}")
print(f"group share of dropped rows: {g_drop/drop:.0%} vs {G/N:.0%} of data")
assert g_drop / G == 0.375 and round((drop-g_drop)/(N-G), 4) == 0.0365
assert g_drop / drop == 0.30
print(f"group share after drop: {(G-g_drop)/(N-drop):.2%}")
assert round((G-g_drop)/(N-drop), 4) == 0.0263

# --- simulation: three kinds of rows (all distributions invented) ---
rng = np.random.default_rng(41)
grp = np.zeros(N, bool); grp[:G] = True
noisy = rng.random(N) < 0.03                      # 3% wrong labels in both groups
loss = np.where(grp, rng.exponential(0.50, N), rng.exponential(0.10, N))  # group is harder
loss = np.where(noisy, 2.0 + rng.exponential(0.8, N), loss)               # wrong labels: high loss

def report(name, dropped):
    d = int(dropped.sum())
    n_noisy = int((dropped & noisy).sum())
    g_valid = int((dropped & grp & ~noisy).sum())
    print(f"{name:34s} dropped={d:5d} noise_precision={n_noisy/d:.2f} "
          f"noise_recall={n_noisy/noisy.sum():.2f} valid_group_rows_lost={g_valid}")
    return d, n_noisy, g_valid

thr = np.quantile(loss, 0.95)
a = report("A global top-5% loss", loss >= thr)
tg = np.quantile(loss[grp], 0.95); to = np.quantile(loss[~grp], 0.95)
b = report("B per-group top-5% loss", np.where(grp, loss >= tg, loss >= to))
# C: need loss in the top 5% AND a second signal (here: a second model disagrees, simulated
# as firing on 85% of noisy rows and 10% of clean rows). Illustrative second signal.
second = np.where(noisy, rng.random(N) < 0.85, rng.random(N) < 0.10)
c = report("C top-5% loss AND second signal", (loss >= thr) & second)

print(f"A dropped group rows total: {int((loss>=thr)[grp].sum())} of {G}")
assert a[2] > 5 * b[2] > 0 and a[2] > c[2]          # global filter loses most valid group rows
assert c[1] / c[0] > a[1] / a[0]                     # second signal raises noise precision
# group-wise accuracy cost of each policy is not simulated: check it with a real group eval set.
