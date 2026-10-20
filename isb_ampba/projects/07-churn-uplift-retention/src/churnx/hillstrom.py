"""Track B: uplift evaluation on the REAL Hillstrom e-mail randomised experiment (oracle-free, IPW)."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from churnx.policy import bootstrap_value_ci, ipw_value
from churnx.uplift import MetaLearner, bootstrap_ci, qini_auc, qini_curve, uplift_at_k

OUTCOMES = {"visit": "binary", "conversion": "binary", "spend": "cont"}
LEARNERS = ["S", "T", "X", "TO"]
COVARS = ["recency", "history", "mens", "womens", "newbie", "zip_code", "channel"]


def design_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode covariates (pre-treatment only)."""
    return pd.get_dummies(df[COVARS], dtype=float)


def balance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Covariate means by arm (randomisation check) plus the standardised mean difference treated vs control."""
    X = design_matrix(df)
    w = (df["segment"] != "No E-Mail").to_numpy()
    rows = []
    for c in X.columns:
        t, k = X.loc[w, c], X.loc[~w, c]
        sd = np.sqrt((t.var() + k.var()) / 2) or 1.0
        rows.append({"covariate": c, "mean_treated": float(t.mean()), "mean_control": float(k.mean()),
                     "std_diff": float((t.mean() - k.mean()) / sd)})
    return pd.DataFrame(rows)


def run_hillstrom(df: pd.DataFrame, cfg: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """S/T/X/TO learners per outcome on a 50/50 split, Qini (+bootstrap CI), and IPW policy values (profit/1000).

    Returns (json-serialisable results, extras with Qini curves for plotting).
    """
    hc, seed = cfg["hillstrom"], cfg["seed"]
    df = df.reset_index(drop=True)
    df["w"] = (df["segment"] != "No E-Mail").astype(int)
    X = design_matrix(df)
    tr, te = train_test_split(df.index, test_size=hc["test_size"], random_state=seed, stratify=df["segment"])
    e = float(df["w"].mean())
    params = {"n_estimators": 150, "num_leaves": 8, "min_child_samples": 100, "learning_rate": 0.03,
              "subsample": 0.8, "colsample_bytree": 0.8}
    res: dict[str, Any] = {"n": int(len(df)), "n_test": int(len(te)), "propensity": e,
                           "arm_means": df.groupby("segment")[["visit", "conversion", "spend"]].mean().round(4).to_dict("index"),
                           "learners": {}, "policies": {}}
    scores: dict[str, dict[str, np.ndarray]] = {}
    rng_seed = seed
    for out, kind in OUTCOMES.items():
        y_te, w_te = df.loc[te, out].to_numpy(float), df.loc[te, "w"].to_numpy()
        scores[out] = {}
        res["learners"][out] = {}
        for L in LEARNERS:
            m = MetaLearner(L, "binary" if kind == "binary" else "cont", params, seed, e=e)
            m.fit(X.loc[tr], df.loc[tr, "w"], df.loc[tr, out])
            s = m.predict(X.loc[te])
            scores[out][L] = s
            lo, hi = bootstrap_ci(lambda idx, s=s: qini_auc(y_te[idx], w_te[idx], s[idx]), len(te),
                                  hc["n_boot"], rng_seed)
            res["learners"][out][L] = {"qini": qini_auc(y_te, w_te, s), "qini_ci95": [lo, hi],
                                       "uplift_at_30": uplift_at_k(y_te, w_te, s, 0.3)}
        rnd = np.random.default_rng(seed).random(len(te))
        res["learners"][out]["random"] = {"qini": qini_auc(y_te, w_te, rnd),
                                          "qini_ci95": list(bootstrap_ci(lambda idx: qini_auc(y_te[idx], w_te[idx], rnd[idx]),
                                                                         len(te), hc["n_boot"], rng_seed)),
                                          "uplift_at_30": uplift_at_k(y_te, w_te, rnd, 0.3)}
    # IPW policy value on held-out half: revenue outcome = spend * margin; cost per e-mail.
    money = df.loc[te, "spend"].to_numpy(float) * hc["margin_on_spend"]
    w_te = df.loc[te, "w"].to_numpy()
    cost = hc["email_cost_usd"]
    # choose the policy learner on a validation slice of the TRAIN half (never on the evaluation half)
    tr2, va = train_test_split(tr, test_size=0.25, random_state=seed, stratify=df.loc[tr, "segment"])
    val_q = {}
    for L in LEARNERS:
        mv = MetaLearner(L, "cont", params, seed, e=e).fit(X.loc[tr2], df.loc[tr2, "w"], df.loc[tr2, "spend"])
        val_q[L] = qini_auc(df.loc[va, "spend"].to_numpy(float), df.loc[va, "w"].to_numpy(), mv.predict(X.loc[va]))
    best_L = max(val_q, key=val_q.get)
    res["policy_learner_val_qini"] = val_q
    tau_money = scores["spend"][best_L] * hc["margin_on_spend"]
    n = len(te)
    k = int(round(0.3 * n))
    top = np.zeros(n, bool)
    top[np.argsort(-tau_money, kind="mergesort")[:k]] = True
    rnd_mask = np.zeros(n, bool)
    rnd_mask[np.random.default_rng(seed).permutation(n)[:k]] = True
    hist = df.loc[te, "history"].to_numpy(float)
    hist_mask = np.zeros(n, bool)
    hist_mask[np.argsort(-hist, kind="mergesort")[:k]] = True
    masks = {"random_30": rnd_mask, "all": np.ones(n, bool), "history_top_30": hist_mask,
             "uplift_top_30": top, "uplift_profit_optimal": (tau_money - cost) > 0}
    for name, m in masks.items():
        f = lambda idx, m=m: 1000 * ipw_value(m[idx], w_te[idx], money[idx], e, cost) / len(idx)  # noqa: E731
        lo, hi = bootstrap_value_ci(f, n, hc["n_boot"], seed)
        res["policies"][name] = {"profit_per_1000_usd": f(np.arange(n)), "ci95": [lo, hi], "n_treated": int(m.sum())}
    res["uplift_learner_for_policy"] = best_L
    extras = {"qini_curves": {o: {L: qini_curve(df.loc[te, o].to_numpy(float), w_te, scores[o][L]) for L in LEARNERS}
                              for o in OUTCOMES}}
    return res, extras
