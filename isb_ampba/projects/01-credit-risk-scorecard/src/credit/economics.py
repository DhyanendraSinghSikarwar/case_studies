"""Expected loss / profit, cut-off optimisation, sensitivity and the limit-action engine."""
from __future__ import annotations

import numpy as np
import pandas as pd


def cutoff_grid(cfg: dict) -> np.ndarray:
    """Cut-off grid from config (inclusive of stop)."""
    g = cfg["economics"]["cutoff_grid"]
    return np.round(np.arange(g["start"], g["stop"] + g["step"] / 2, g["step"]), 6)


def make_ead(limit_bal, avg_util, fx: float = 1.0, floor_util: float = 0.05) -> np.ndarray:
    """EAD = LIMIT_BAL * avg_util (utilisation floored at 5%, capped at 150%) * fx."""
    util = np.clip(np.asarray(avg_util, dtype=float), floor_util, 1.5)
    return np.asarray(limit_bal, dtype=float) * util * fx


def expected_loss(pd_, lgd: float, ead) -> np.ndarray:
    """EL = PD * LGD * EAD."""
    return np.asarray(pd_, dtype=float) * lgd * np.asarray(ead, dtype=float)


def unit_profit(pd_, ead, margin: float, lgd: float) -> np.ndarray:
    """Expected profit per approved account: (1-PD)*margin*EAD - PD*LGD*EAD."""
    pd_, ead = np.asarray(pd_, dtype=float), np.asarray(ead, dtype=float)
    return (1 - pd_) * margin * ead - pd_ * lgd * ead


def realised_profit(y, ead, margin: float, lgd: float) -> np.ndarray:
    """Profit using the actual outcome y."""
    y, ead = np.asarray(y, dtype=float), np.asarray(ead, dtype=float)
    return (1 - y) * margin * ead - y * lgd * ead


def profit_curve(pd_, ead, y, margin: float, lgd: float, grid) -> pd.DataFrame:
    """Sweep the approve-if-PD<=cutoff policy."""
    pd_, ead, y = map(np.asarray, (pd_, ead, y))
    up, rp = unit_profit(pd_, ead, margin, lgd), realised_profit(y, ead, margin, lgd)
    rows = []
    for c in grid:
        m = pd_ <= c
        n = int(m.sum())
        rows.append({"cutoff": float(c), "approval_rate": n / len(pd_),
                     "bad_rate_approved": float(y[m].mean()) if n else np.nan,
                     "exp_profit": float(up[m].sum()), "real_profit": float(rp[m].sum())})
    return pd.DataFrame(rows)


def find_optimal_cutoff(curve: pd.DataFrame, col: str = "exp_profit") -> pd.Series:
    """Row of the profit curve with maximum `col`."""
    return curve.loc[curve[col].idxmax()]


def sensitivity_grid(pd_, ead, y, lgds, margins, grid) -> pd.DataFrame:
    """Optimal cut-off and uplift vs approve-all for each LGD x margin cell."""
    rows = []
    for lgd in lgds:
        for mg in margins:
            best = find_optimal_cutoff(profit_curve(pd_, ead, y, mg, lgd, grid))
            approve_all = float(unit_profit(pd_, ead, mg, lgd).sum())
            rows.append({"lgd": lgd, "margin": mg, "opt_cutoff": best["cutoff"], "exp_profit": best["exp_profit"],
                         "approve_all": approve_all, "uplift": best["exp_profit"] - approve_all})
    return pd.DataFrame(rows)


def limit_action(band: str, limits_cfg: dict) -> dict:
    """Action for a risk band, from config: {action, limit_change, pd_mult}."""
    return dict(limits_cfg[band])


def limit_engine_value(bands, pd_, ead, margin: float, lgd: float, limits_cfg: dict) -> pd.DataFrame:
    """Profit change per band if the config's limit action is applied (EAD scales with limit change, PD with pd_mult)."""
    df = pd.DataFrame({"band": np.asarray(bands), "pd": np.asarray(pd_), "ead": np.asarray(ead)})
    out = []
    for b, g in df.groupby("band"):
        a = limits_cfg[b]
        before = unit_profit(g["pd"], g["ead"], margin, lgd).sum()
        if a["action"] == "decline":
            after = 0.0
        else:
            after = unit_profit(np.clip(g["pd"] * a["pd_mult"], 0, 1), g["ead"] * (1 + a["limit_change"]),
                                margin, lgd).sum()
        out.append({"band": b, "n": len(g), "action": a["action"], "profit_before": float(before),
                    "profit_after": float(after), "delta": float(after - before)})
    return pd.DataFrame(out).sort_values("band").reset_index(drop=True)
