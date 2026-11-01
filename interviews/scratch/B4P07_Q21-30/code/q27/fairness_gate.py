"""Per-slice gate: selection-rate ratio, TPR gap, FPR gap, no-worse-than-champion. Exit 1 on failure."""
import sys

import numpy as np
import pandas as pd

MIN_GROUP = 200
MIN_RATIO = 0.80      # illustrative four-fifths style threshold, NOT a legal standard
MAX_TPR_GAP = 0.10
MAX_FPR_GAP = 0.10
SLICE_TOL = 0.02      # candidate TPR may be at most this much below champion, per slice


def make_data(seed=0, n=6000):
    rng = np.random.default_rng(seed)
    group = rng.choice(["A", "B", "C"], size=n, p=[0.55, 0.35, 0.10])
    y = rng.binomial(1, 0.30, n)
    signal = y * 1.5 + rng.normal(0, 1, n)
    return pd.DataFrame({"group": group, "y": y, "signal": signal})


def predictions(df, shift_by_group):
    """Decision = signal above 0.9, plus a group-specific shift (the unfairness knob)."""
    s = df["signal"] + df["group"].map(shift_by_group).fillna(0.0)
    return (s > 0.9).astype(int)


def group_metrics(df, pred):
    rows = {}
    for g, d in df.assign(pred=pred).groupby("group"):
        pos, neg = d[d.y == 1], d[d.y == 0]
        rows[g] = {"n": len(d), "sel": d.pred.mean(), "tpr": pos.pred.mean(), "fpr": neg.pred.mean()}
    return pd.DataFrame(rows).T


def gate(df, cand_pred, champ_pred):
    cm, hm = group_metrics(df, cand_pred), group_metrics(df, champ_pred)
    fails = []
    for g, r in cm.iterrows():
        if r.n < MIN_GROUP:
            fails.append(f"group {g}: n={int(r.n)} < {MIN_GROUP}, too small to judge (manual review)")
    ok = cm[cm.n >= MIN_GROUP]
    ratio = ok.sel.min() / ok.sel.max()
    if ratio < MIN_RATIO:
        fails.append(f"selection-rate ratio {ratio:.2f} < {MIN_RATIO} ({ok.sel.idxmin()} vs {ok.sel.idxmax()})")
    if ok.tpr.max() - ok.tpr.min() > MAX_TPR_GAP:
        fails.append(f"TPR gap {ok.tpr.max() - ok.tpr.min():.2f} > {MAX_TPR_GAP}")
    if ok.fpr.max() - ok.fpr.min() > MAX_FPR_GAP:
        fails.append(f"FPR gap {ok.fpr.max() - ok.fpr.min():.2f} > {MAX_FPR_GAP}")
    for g in ok.index:
        if cm.loc[g, "tpr"] < hm.loc[g, "tpr"] - SLICE_TOL:
            fails.append(f"group {g}: TPR {cm.loc[g, 'tpr']:.2f} worse than champion {hm.loc[g, 'tpr']:.2f}")
    return cm, fails


if __name__ == "__main__":
    which = sys.argv[1]  # fair | unfair
    df = make_data()
    champ = predictions(df, {})
    cand = predictions(df, {} if which == "fair" else {"C": -0.9})
    cm, fails = gate(df, cand, champ)
    print(f"candidate = {which}")
    print(cm.round(3).to_string())
    for f in fails:
        print("FAIL", f)
    print("GATE:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
