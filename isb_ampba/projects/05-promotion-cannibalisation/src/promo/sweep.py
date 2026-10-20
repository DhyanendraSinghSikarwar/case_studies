"""Latin-hypercube sweep of the uncertain assumptions on a normalised parametric engine."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import qmc

PARAMS = ["elasticity", "substitution_share", "margin", "halo"]


def param_ranges(cfg: dict) -> tuple[np.ndarray, np.ndarray]:
    """(lo, hi) arrays for [elasticity, substitution_share, margin, halo] from config."""
    sw = cfg["sweep"]
    lo = np.array([sw["elasticity"][0], sw["substitution_share"][0], sw["margin"][0], sw["halo"][0]], float)
    hi = np.array([sw["elasticity"][1], sw["substitution_share"][1], sw["margin"][1], sw["halo"][1]], float)
    # config gives elasticity as [-6, -1]: ensure lo < hi for scaling
    return np.minimum(lo, hi), np.maximum(lo, hi)


def draw_conditions(cfg: dict, n: int | None = None, seed: int | None = None) -> pd.DataFrame:
    """Latin-hypercube draws (seeded) scaled to the configured ranges."""
    n = cfg["sweep"]["n_draws"] if n is None else n
    seed = cfg["seed"] if seed is None else seed
    u = qmc.LatinHypercube(d=4, seed=seed).random(n)
    lo, hi = param_ranges(cfg)
    return pd.DataFrame(qmc.scale(u, lo, hi), columns=PARAMS)


def parametric_scores(eps, sub, margin, halo, d: float, halo_ref_ratio: float, u0: float = 1.0, p: float = 1.0) -> dict:
    """Parametric engine (vectorised) per unit of baseline weekly sales; money terms scale linearly in u0*p.

    delta = u0 ((1-d)^eps - 1); direct = delta (p(1-d) - (1-m)p); subsidy = d p u0;
    cannibalised = s delta m p; halo = h delta m p halo_ref_ratio (basket revenue per unit relative to own price).
    """
    eps, sub, margin, halo = (np.asarray(x, float) for x in (eps, sub, margin, halo))
    delta = u0 * ((1 - d) ** eps - 1)
    direct = delta * (p * (1 - d) - (1 - margin) * p)
    subsidy = np.full_like(direct, d * p * u0)
    cannibalised = sub * delta * margin * p
    halo_m = halo * delta * margin * p * halo_ref_ratio
    return {
        "direct_uplift": direct, "subsidy_cost": subsidy, "cannibalised_margin": cannibalised, "halo_margin": halo_m,
        "promoted_only": direct - subsidy, "family_net": direct - subsidy - cannibalised + halo_m,
    }


def run_sweep(cfg: dict, d: float, halo_ref_ratio: float, n: int | None = None, seed: int | None = None) -> pd.DataFrame:
    """Draw conditions and score them; adds break-even elasticity per draw."""
    draws = draw_conditions(cfg, n, seed)
    sc = parametric_scores(draws["elasticity"], draws["substitution_share"], draws["margin"], draws["halo"], d, halo_ref_ratio)
    out = draws.copy()
    for k, v in sc.items():
        out[k] = v
    out["promoted_only_profitable"] = out["promoted_only"] > 0
    out["family_profitable"] = out["family_net"] > 0
    out["dashboard_trap"] = out["promoted_only_profitable"] & ~out["family_profitable"]
    out["break_even_elasticity"] = [
        parametric_break_even(s, m, h, d, halo_ref_ratio, tuple(cfg["sweep"]["breakeven_bounds"]))
        for s, m, h in zip(out["substitution_share"], out["margin"], out["halo"])
    ]
    return out


def parametric_break_even(sub: float, margin: float, halo: float, d: float, halo_ref_ratio: float, bounds: tuple[float, float] = (-12.0, -0.5)) -> float:
    """Elasticity at which parametric family net = 0 (NaN if no sign change in bounds)."""
    def f(e: float) -> float:
        return float(parametric_scores(e, sub, margin, halo, d, halo_ref_ratio)["family_net"])

    fa, fb = f(bounds[0]), f(bounds[1])
    if fa * fb > 0:
        return float("nan")
    return float(brentq(f, bounds[0], bounds[1], xtol=1e-10))


def sweep_summary(df: pd.DataFrame) -> dict:
    """Headline shares: % profitable promoted-only vs family, dashboard-trap share, break-even distribution."""
    be = df["break_even_elasticity"].dropna()
    return {
        "n_draws": int(len(df)),
        "pct_promoted_only_profitable": float(100 * df["promoted_only_profitable"].mean()),
        "pct_family_profitable": float(100 * df["family_profitable"].mean()),
        "pct_dashboard_trap": float(100 * df["dashboard_trap"].mean()),
        "pct_family_profitable_given_promoted_only_profitable": float(100 * df.loc[df["promoted_only_profitable"], "family_profitable"].mean()) if df["promoted_only_profitable"].any() else float("nan"),
        "break_even_elasticity_n": int(len(be)),
        "break_even_elasticity_median": float(be.median()) if len(be) else float("nan"),
        "break_even_elasticity_p10": float(be.quantile(0.10)) if len(be) else float("nan"),
        "break_even_elasticity_p90": float(be.quantile(0.90)) if len(be) else float("nan"),
        "pct_never_breaks_even_in_range": float(100 * df["break_even_elasticity"].isna().mean()),
    }


def tornado(cfg: dict, d: float, halo_ref_ratio: float) -> pd.DataFrame:
    """One-at-a-time swing of family net around the mid-point base case, plus profitable share by half-range."""
    lo, hi = param_ranges(cfg)
    base = (lo + hi) / 2
    draws = draw_conditions(cfg)
    fn_all = parametric_scores(draws["elasticity"], draws["substitution_share"], draws["margin"], draws["halo"], d, halo_ref_ratio)["family_net"]
    rows = []
    for k, name in enumerate(PARAMS):
        vals = {}
        for tag, v in (("low", lo[k]), ("high", hi[k])):
            x = base.copy(); x[k] = v
            vals[tag] = float(parametric_scores(*x, d, halo_ref_ratio)["family_net"])
        mid = (lo[k] + hi[k]) / 2
        below = draws[name] < mid
        rows.append({
            "param": name, "low_value": lo[k], "high_value": hi[k], "net_at_low": vals["low"], "net_at_high": vals["high"],
            "swing": abs(vals["high"] - vals["low"]),
            "pct_profitable_lower_half": float(100 * (fn_all[below] > 0).mean()),
            "pct_profitable_upper_half": float(100 * (fn_all[~below] > 0).mean()),
        })
    t = pd.DataFrame(rows)
    t["flip_gap_pts"] = (t["pct_profitable_upper_half"] - t["pct_profitable_lower_half"]).abs()
    base_net = float(parametric_scores(*base, d, halo_ref_ratio)["family_net"])
    t.attrs["base_net"] = base_net
    return t.sort_values("swing", ascending=False).reset_index(drop=True)


def heatmap_grid(cfg: dict, d: float, halo_ref_ratio: float, x_param: str = "substitution_share", n: int = 25) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Family net on an elasticity x x_param grid, other parameters at mid-point."""
    lo, hi = param_ranges(cfg)
    base = dict(zip(PARAMS, (lo + hi) / 2))
    ei = PARAMS.index("elasticity"); xi = PARAMS.index(x_param)
    es = np.linspace(lo[ei], hi[ei], n); xs = np.linspace(lo[xi], hi[xi], n)
    E, X = np.meshgrid(es, xs, indexing="ij")
    args = {k: np.full_like(E, v) for k, v in base.items()}
    args["elasticity"] = E; args[x_param] = X
    z = parametric_scores(args["elasticity"], args["substitution_share"], args["margin"], args["halo"], d, halo_ref_ratio)["family_net"]
    return es, xs, z


def classification_accuracy(cfg: dict, d: float, halo_ref_ratio: float, seed: int | None = None) -> dict:
    """KPI: % of proposed promos correctly classified profitable/unprofitable vs simulation truth.

    Truth = family_net > 0 at the drawn (true) parameters. Dashboard rule = promoted-only > 0.
    Engine = family_net > 0 evaluated with parameters known only up to multiplicative noise (relative sd per level).
    """
    seed = cfg["seed"] if seed is None else seed
    rng = np.random.default_rng(seed)
    draws = draw_conditions(cfg)
    t = parametric_scores(draws["elasticity"], draws["substitution_share"], draws["margin"], draws["halo"], d, halo_ref_ratio)
    truth = t["family_net"] > 0
    out = {"dashboard_accuracy_pct": float(100 * ((t["promoted_only"] > 0) == truth).mean())}
    for sd in cfg["kpi"]["noise_levels"]:
        noisy = {}
        for name in PARAMS:
            v = draws[name].to_numpy() * (1 + rng.normal(0, sd, len(draws)))
            noisy[name] = np.minimum(v, -0.05) if name == "elasticity" else np.clip(v, 0, None)
        n = parametric_scores(noisy["elasticity"], noisy["substitution_share"], noisy["margin"], noisy["halo"], d, halo_ref_ratio)
        out[f"engine_accuracy_pct_noise_{int(round(sd * 100))}"] = float(100 * ((n["family_net"] > 0) == truth).mean())
    return out
