"""Promotion engine: score a discount on family net contribution; break-even elasticity; engine context."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from .demand import mnl_after_discount

TERMS = ["direct_uplift", "subsidy_cost", "cannibalised_margin", "halo_margin"]


def score_promo(
    u: np.ndarray, p: np.ndarray, i: int, d: float, eps_i: float, margin: float,
    halo_per_unit: float, halo_margin_per_unit: float, cfg: dict,
    sub_weight: float = 1.0, halo_factor: float | None = None, outside_share: float | None = None,
    nest_lambda: float | None = None,
) -> dict:
    """Score discount d on SKU i of a family. All money in GBP over ``promo_weeks`` weeks.

    u, p: baseline weekly units and list prices of the family members; margin: unit margin as share of price
    (unit cost = (1-margin) * p, an assumption: the data has no costs); halo_per_unit: basket-rule units per
    incremental unit; halo_margin_per_unit: basket-rule margin per incremental unit (GBP).
    family_net is the sum of the four terms by construction.
    """
    u = np.asarray(u, float); p = np.asarray(p, float)
    W = cfg["engine"]["promo_weeks"]
    hf = cfg["engine"]["halo_factor"] if halo_factor is None else halo_factor
    os_ = cfg["demand"]["outside_share"] if outside_share is None else outside_share
    c = (1 - margin) * p
    nl = cfg["demand"].get("nest_lambda", 1.0) if nest_lambda is None else nest_lambda
    u2 = mnl_after_discount(u, p, i, d, eps_i, os_, sub_weight, nl)
    p_i2 = p[i] * (1 - d)
    delta_i = (u2[i] - u[i]) * W
    direct = delta_i * (p_i2 - c[i])
    subsidy = d * p[i] * u[i] * W
    sib = np.arange(len(u)) != i
    cannibalised = float((np.maximum(u[sib] - u2[sib], 0.0) * W * (p[sib] - c[sib])).sum())
    halo = hf * delta_i * halo_margin_per_unit
    net = direct - subsidy - cannibalised + halo
    return {
        "direct_uplift": float(direct), "subsidy_cost": float(subsidy), "cannibalised_margin": cannibalised,
        "halo_margin": float(halo), "promoted_only": float(direct - subsidy), "family_net": float(net),
        "incremental_units": float(delta_i), "halo_units": float(hf * delta_i * halo_per_unit),
        "units_after": u2, "sibling_units_lost": float(np.maximum(u[sib] - u2[sib], 0.0).sum() * W),
    }


def break_even_elasticity(
    u: np.ndarray, p: np.ndarray, i: int, d: float, margin: float, halo_per_unit: float, halo_margin_per_unit: float,
    cfg: dict, sub_weight: float = 1.0, halo_factor: float | None = None, outside_share: float | None = None,
    bounds: tuple[float, float] = (-12.0, -0.5), nest_lambda: float | None = None,
) -> float:
    """Elasticity at which family_net = 0 (brentq on bounds); NaN when the sign never changes in range."""
    def f(eps: float) -> float:
        return score_promo(u, p, i, d, eps, margin, halo_per_unit, halo_margin_per_unit, cfg, sub_weight, halo_factor, outside_share, nest_lambda)["family_net"]

    if d <= 0:
        return float("nan")
    fa, fb = f(bounds[0]), f(bounds[1])
    if not (np.isfinite(fa) and np.isfinite(fb)) or fa * fb > 0:
        return float("nan")
    return float(brentq(f, bounds[0], bounds[1], xtol=1e-10))


@dataclass
class EngineContext:
    """SKU-level engine inputs (one row per SKU) with convenience scoring methods."""

    table: pd.DataFrame
    cfg: dict
    _by_fam: dict = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self.table = self.table.set_index("stock_code", drop=False)
        self.table.index.name = None
        act = self.table[self.table["active"]]
        self._by_fam = {f: g.index.to_list() for f, g in act.groupby("family")}

    def members(self, sku: str) -> list[str]:
        """Active family members of ``sku`` (always includes sku itself, first)."""
        fam = self.table.at[sku, "family"]
        mem = [m for m in self._by_fam.get(fam, []) if m != sku]
        return [sku] + mem

    def arrays(self, sku: str) -> tuple[list[str], np.ndarray, np.ndarray]:
        """(member codes, baseline units, prices); promoted SKU is index 0."""
        mem = self.members(sku)
        t = self.table.loc[mem]
        return mem, t["base_units"].to_numpy(float), t["list_price"].to_numpy(float)

    def score(self, sku: str, d: float, eps: float | None = None, margin: float | None = None,
              halo_factor: float | None = None, outside_share: float | None = None, sub_weight: float | None = None,
              nest_lambda: float | None = None) -> dict:
        """Score discount d on SKU using the family, elasticity and halo stored in the table (overridable)."""
        mem, u, p = self.arrays(sku)
        r = self.table.loc[sku]
        m = 1 - self.cfg["engine"]["unit_cost_share"] if margin is None else margin
        sw = float(r["sub_weight"]) if sub_weight is None else sub_weight
        e = float(r["eps"]) if eps is None else eps
        hu = float(r.get("halo_units", 0.0) or 0.0)
        hr = float(r.get("halo_rev_per_unit", 0.0) or 0.0)
        out = score_promo(u, p, 0, d, e, m, hu, m * hr, self.cfg, sw, halo_factor, outside_share, nest_lambda)
        out["members"] = mem; out["baseline_units"] = u; out["prices"] = p; out["eps"] = e; out["margin"] = m
        return out

    def break_even(self, sku: str, d: float, margin: float | None = None, halo_factor: float | None = None,
                   outside_share: float | None = None, sub_weight: float | None = None,
                   nest_lambda: float | None = None) -> float:
        """Break-even elasticity for the SKU's family at discount d."""
        mem, u, p = self.arrays(sku)
        r = self.table.loc[sku]
        m = 1 - self.cfg["engine"]["unit_cost_share"] if margin is None else margin
        sw = float(r["sub_weight"]) if sub_weight is None else sub_weight
        hu = float(r.get("halo_units", 0.0) or 0.0); hr = float(r.get("halo_rev_per_unit", 0.0) or 0.0)
        return break_even_elasticity(u, p, 0, d, m, hu, m * hr, self.cfg, sw, halo_factor, outside_share,
                                     tuple(self.cfg["sweep"]["breakeven_bounds"]), nest_lambda)


def reference_promo(ctx: EngineContext, skus: list[str], d: float, **kw: float) -> pd.DataFrame:
    """Score the same discount for several SKUs: waterfall terms, promoted-only vs family view, break-even elasticity."""
    rows = []
    for s in skus:
        r = ctx.score(s, d, **kw)
        be = ctx.break_even(s, d, **{k: v for k, v in kw.items() if k in ("margin", "halo_factor", "outside_share", "sub_weight", "nest_lambda")})
        t = ctx.table.loc[s]
        rows.append({
            "stock_code": s, "description": t["description"], "family": t["family"], "n_family_active": len(r["members"]),
            "eps": r["eps"], "eps_source": t["eps_source"], "weekly_revenue": t["weekly_revenue"],
            **{k: r[k] for k in TERMS}, "promoted_only": r["promoted_only"], "family_net": r["family_net"],
            "incremental_units": r["incremental_units"], "break_even_eps": be,
            "break_even_multiplier": be / r["eps"] if np.isfinite(be) else float("nan"),
        })
    df = pd.DataFrame(rows)
    df["looks_profitable_promoted_only"] = df["promoted_only"] > 0
    df["profitable_family"] = df["family_net"] > 0
    return df
