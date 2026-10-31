import numpy as np, pandas as pd

rng = np.random.default_rng(28)
GROUPS = {"A": 0.70, "B": 0.27, "C": 0.03}          # traffic share; C is tiny
rows = []
for w in range(1, 5):                                 # four weekly windows, 4000 decisions each
    n = 4000
    g = rng.choice(list(GROUPS), n, p=list(GROUPS.values()))
    skill = rng.normal(0, 1, n)
    y = (rng.random(n) < 1 / (1 + np.exp(-(skill - 0.3)))).astype(int)      # true outcome
    score = skill + rng.normal(0, 0.7, n)
    penalty = np.where((g == "B") & (w >= 3), 0.9, 0.0)                       # from week 3 the model under-scores group B
    approve = ((score - penalty) > 0.4).astype(int)
    rows.append(pd.DataFrame({"week": w, "group": g, "approve": approve, "y": y}))
df = pd.concat(rows, ignore_index=True)

def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

REF, MIN_N, RATIO = "A", 200, 0.8
out = []
for w, d in df.groupby("week"):
    ref = d[d.group == REF]
    ref_sel = ref.approve.mean()
    ref_pos = ref[ref.y == 1]; ref_tpr = ref_pos.approve.mean()
    for g, x in d.groupby("group"):
        sel = x.approve.mean(); lo, hi = wilson(x.approve.sum(), len(x))
        pos = x[x.y == 1]; tpr = pos.approve.mean()
        naive = sel / ref_sel < RATIO
        # alert only if the group is big enough AND even the upper end of its interval is below the ratio line
        guarded = len(x) >= MIN_N and (hi / ref_sel < RATIO)
        out.append(dict(week=w, group=g, n=len(x), sel=round(sel, 3), ci=f"[{lo:.2f},{hi:.2f}]",
                        ratio=round(sel / ref_sel, 2), tpr_gap=round(tpr - ref_tpr, 3), naive_alert=naive, guarded_alert=guarded))
res = pd.DataFrame(out)
print(res.to_string(index=False))
print("\nweeks where naive rule fired for C (tiny group):", res[(res.group == "C") & res.naive_alert].week.tolist())
print("weeks where guarded rule fired:", res[res.guarded_alert][["week", "group"]].values.tolist())
