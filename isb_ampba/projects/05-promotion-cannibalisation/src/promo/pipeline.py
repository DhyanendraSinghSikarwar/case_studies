"""End-to-end pipeline stages (data -> engine table -> evaluation) used by tasks.py, analysis and the e2e test."""
from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from . import viz
from .baskets import basket_matrix, halo_table, mine_rules
from .catalog import apply_overrides, build_families, copurchase_share, substitution_weights
from .config import ROOT, get_logger, load_config, path_for, seed_everything
from .data import clean_sales, price_variation_report, sku_descriptions, weekly_panel
from .demand import baseline_table, estimate_elasticities, mnl_shares_after_discount, pooled_fe_elasticity, seasonal_index
from .engine import EngineContext, reference_promo
from .optimise import (
    budget_from,
    candidate_table,
    dashboard_plan,
    optimise_calendar,
    optimise_single,
    plan_summary,
)
from .sweep import classification_accuracy, heatmap_grid, run_sweep, sweep_summary, tornado

log = get_logger("promo.pipeline")


def to_py(o):
    """Recursively convert numpy / pandas scalars for JSON."""
    if isinstance(o, dict):
        return {str(k): to_py(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_py(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp,)):
        return str(o.date())
    return o


# --------------------------------------------------------------------------- train stage
def build_engine_table(sales: pd.DataFrame, panel: pd.DataFrame, cfg: dict, overrides: str | Path | None = None,
                       as_of: pd.Timestamp | None = None) -> dict:
    """Families, co-purchase check, basket halo, elasticities and baselines merged into one SKU table.

    Everything is computed from data up to ``as_of`` (default: all data).
    """
    if as_of is not None:
        sales = sales[sales["week"] <= as_of]
        panel = panel[panel["week"] <= as_of]
    desc = sku_descriptions(sales)
    base = baseline_table(panel, cfg, as_of)
    fam = apply_overrides(build_families(desc, cfg), overrides if overrides is not None else cfg["families"]["overrides_csv"])
    cop = copurchase_share(sales, fam, cfg)
    fam = substitution_weights(fam, cop, cfg)
    fam_of = dict(zip(fam["stock_code"], fam["family"]))
    price_of = dict(zip(base["stock_code"], base["list_price"]))
    basket = basket_matrix(sales, cfg["baskets"]["top_skus"])
    rules = mine_rules(basket, fam_of, cfg)
    halo = halo_table(rules, price_of)
    elas = estimate_elasticities(panel, fam_of, cfg)
    elig = elas.loc[elas["eligible"], "stock_code"]
    pooled = pooled_fe_elasticity(panel[panel["stock_code"].isin(elig)]) if len(elig) else {"eps": float("nan"), "se": float("nan"), "n_obs": 0}
    table = (
        fam.merge(base, on="stock_code", how="inner")
        .merge(halo, on="stock_code", how="left")
        .merge(elas[["stock_code", "eps", "eps_hat", "se", "eps_source", "eligible", "valid", "positive", "n_drops", "n_weeks"]], on="stock_code", how="left")
    )
    for c in ("halo_units", "halo_rev_per_unit", "n_rules"):
        table[c] = table[c].fillna(0.0)
    table["eps"] = table["eps"].fillna(cfg["demand"]["prior_elasticity"])
    table["eps_source"] = table["eps_source"].fillna("prior")
    return {"table": table, "families": fam, "copurchase": cop, "rules": rules, "elasticities": elas, "pooled": pooled, "basket_shape": basket.shape}


def train_summary(res: dict, cfg: dict) -> dict:
    """Numbers describing families, co-purchase, baskets and demand estimates."""
    t, fam, cop, el = res["table"], res["families"], res["copurchase"], res["elasticities"]
    fams = fam.drop_duplicates("family")
    multi = fams[fams["n_members"] >= cfg["families"]["min_family_size"]]
    ev = el[el["valid"]]
    return {
        "families": {
            "n_skus": int(len(fam)), "n_families": int(len(fams)), "n_multi_sku_families": int(len(multi)),
            "n_skus_in_multi_families": int(multi["n_members"].sum()), "max_family_size": int(fams["n_members"].max()),
            "median_multi_family_size": float(multi["n_members"].median()) if len(multi) else float("nan"),
            "copurchase_n_families_checked": int(len(cop)),
            "copurchase_median_share": float(cop["copurchase_share"].median()) if len(cop) else float("nan"),
            "copurchase_mean_share": float(cop["copurchase_share"].mean()) if len(cop) else float("nan"),
            "n_weak_substitute_families": int(cop["weak_substitute"].sum()) if len(cop) else 0,
            "pct_weak_substitute_families": float(100 * cop["weak_substitute"].mean()) if len(cop) else float("nan"),
        },
        "baskets": {"matrix_shape": list(res["basket_shape"]), "n_rules": int(len(res["rules"])),
                    "n_skus_with_halo": int((t["halo_units"] > 0).sum()),
                    "median_halo_units_per_unit_where_positive": float(t.loc[t["halo_units"] > 0, "halo_units"].median()) if (t["halo_units"] > 0).any() else 0.0},
        "demand": {
            "n_skus": int(len(el)), "n_eligible": int(el["eligible"].sum()), "n_valid_negative": int(el["valid"].sum()),
            "n_positive_dropped": int(el["positive"].sum()),
            "eps_hat_median": float(ev["eps_hat"].median()) if len(ev) else float("nan"),
            "eps_hat_p10": float(ev["eps_hat"].quantile(0.1)) if len(ev) else float("nan"),
            "eps_hat_p90": float(ev["eps_hat"].quantile(0.9)) if len(ev) else float("nan"),
            "tau2": float(el.attrs.get("tau2", float("nan"))),
            "source_counts": {k: int(v) for k, v in el["eps_source"].value_counts().items()},
            "final_eps_median": float(el["eps"].median()),
            "pooled_two_way_fe": res["pooled"],
            "prior_elasticity": cfg["demand"]["prior_elasticity"],
        },
    }


def save_train_artifacts(res: dict, cfg: dict, out_dir: Path, models_dir: Path | None = None) -> None:
    """Persist the engine table (the app reads it) and supporting CSVs."""
    out_dir.mkdir(parents=True, exist_ok=True)
    res["table"].to_parquet(out_dir / "engine_inputs.parquet", index=False)
    res["families"][["stock_code", "description", "family", "family_name", "n_members"]].to_csv(out_dir / "families.csv", index=False)
    res["copurchase"].to_csv(out_dir / "family_copurchase.csv", index=False)
    res["rules"].to_csv(out_dir / "basket_rules.csv", index=False)
    res["elasticities"].drop(columns=["family"], errors="ignore").to_csv(out_dir / "elasticities.csv", index=False)
    if models_dir is not None:
        models_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump({"table": res["table"], "cfg": cfg}, models_dir / "engine_context.joblib")


# --------------------------------------------------------------------------- evaluation stage
def _mnl_checks(ctx: EngineContext, skus: list[str], cfg: dict) -> dict:
    """Shares sum to one; numerical elasticity from d=0.001 equals eps_i (max relative error)."""
    errs, sums = [], []
    for s in skus:
        mem, u, p = ctx.arrays(s)
        eps = float(ctx.table.at[s, "eps"])
        for d in (0.001, 0.10, 0.25):
            s2, s0, _ = mnl_shares_after_discount(u, p, 0, d, eps, cfg["demand"]["outside_share"])
            sums.append(abs(s2.sum() + s0 - 1.0))
        s2, _, M = mnl_shares_after_discount(u, p, 0, 0.001, eps, cfg["demand"]["outside_share"])
        num = np.log(M * s2[0] / u[0]) / np.log(1 - 0.001)
        errs.append(abs(num / eps - 1))
    return {"max_share_sum_error": float(max(sums)), "max_rel_elasticity_error_d0.001": float(max(errs)), "n_checked": len(skus)}


def evaluate(res: dict, panel: pd.DataFrame, cfg: dict, out_dir: Path, fig_dir: Path) -> dict:
    """Reference promo, sweep, KPI, optimiser and figures. Returns the evaluation part of the summary."""
    out_dir.mkdir(parents=True, exist_ok=True); fig_dir.mkdir(parents=True, exist_ok=True)
    ctx = EngineContext(res["table"].copy(), cfg)
    t = ctx.table
    d_ref = cfg["reference"]["discount"]
    # --- reference promotion: top-N SKUs by total revenue among SKUs active at the end of the data
    ranked = t.sort_values("revenue", ascending=False)
    top_all = ranked.head(cfg["reference"]["top_n"]).index.tolist()
    ref_skus = ranked[ranked["active"]].head(cfg["reference"]["top_n"]).index.tolist()
    ref = reference_promo(ctx, ref_skus, d_ref)
    ref.to_csv(out_dir / "reference_promo.csv", index=False)
    inr = cfg["engine"]["gbp_to_inr"]
    be = ref["break_even_eps"].dropna(); bm = ref["break_even_multiplier"].dropna()
    reference = {
        "discount": d_ref, "n_skus": int(len(ref)), "n_top_by_revenue_inactive_excluded": int(len(set(top_all) - set(ref_skus))),
        "margin_assumed": 1 - cfg["engine"]["unit_cost_share"], "promo_weeks": cfg["engine"]["promo_weeks"],
        "n_looks_profitable_promoted_only": int(ref["looks_profitable_promoted_only"].sum()),
        "n_profitable_family": int(ref["profitable_family"].sum()),
        "n_dashboard_trap": int((ref["looks_profitable_promoted_only"] & ~ref["profitable_family"]).sum()),
        "n_hidden_by_dashboard": int((~ref["looks_profitable_promoted_only"] & ref["profitable_family"]).sum()),
        "promoted_only_total_gbp": float(ref["promoted_only"].sum()), "family_net_total_gbp": float(ref["family_net"].sum()),
        "direct_total_gbp": float(ref["direct_uplift"].sum()), "subsidy_total_gbp": float(ref["subsidy_cost"].sum()),
        "cannibalised_total_gbp": float(ref["cannibalised_margin"].sum()), "halo_total_gbp": float(ref["halo_margin"].sum()),
        "family_net_total_inr": float(ref["family_net"].sum() * inr), "gbp_to_inr": inr,
        "family_net_median_gbp": float(ref["family_net"].median()),
        "n_break_even_defined": int(len(be)), "n_break_even_undefined": int(len(ref) - len(be)),
        "break_even_eps_median": float(be.median()) if len(be) else float("nan"),
        "break_even_eps_min": float(be.min()) if len(be) else float("nan"), "break_even_eps_max": float(be.max()) if len(be) else float("nan"),
        "break_even_multiplier_median": float(bm.median()) if len(bm) else float("nan"),
        "n_estimated_elasticity": int((ref["eps_source"] == "estimated_shrunk").sum()),
        "n_prior_or_family_elasticity": int((ref["eps_source"] != "estimated_shrunk").sum()),
        "mean_family_size_active": float(ref["n_family_active"].mean()),
    }
    sens_rows = []
    rs = cfg["reference_sensitivity"]
    for m in rs["margins"]:
        for o in rs["outside_shares"]:
            r2 = reference_promo(ctx, ref_skus, d_ref, margin=m, outside_share=o)
            sens_rows.append({"margin": m, "outside_share": o, "family_net_total_gbp": float(r2["family_net"].sum()),
                              "promoted_only_total_gbp": float(r2["promoted_only"].sum()), "n_profitable_family": int(r2["profitable_family"].sum())})
    sens = pd.DataFrame(sens_rows); sens.to_csv(out_dir / "reference_sensitivity.csv", index=False)
    # --- sweep
    ratios = ref["stock_code"].map(t["halo_rev_per_unit"]) / ref["stock_code"].map(t["list_price"])
    ratio = float(ratios.median())
    sw = run_sweep(cfg, d_ref, ratio)
    sw.to_csv(out_dir / "sweep_draws.csv", index=False)
    s_sum = sweep_summary(sw)
    sw_by_d = []
    for d in cfg["optimiser"]["discounts"]:
        if d > 0:
            x = run_sweep(cfg, d, ratio)
            sw_by_d.append({"discount": d, **{k: v for k, v in sweep_summary(x).items() if k.startswith("pct_") or k == "break_even_elasticity_median"}})
    pd.DataFrame(sw_by_d).to_csv(out_dir / "sweep_by_discount.csv", index=False)
    sw2 = run_sweep(cfg, d_ref, ratio, seed=cfg["seed"])
    s_sum["reproducible_with_seed"] = bool(sw.equals(sw2))
    s_sum["halo_ref_ratio"] = ratio; s_sum["halo_ref_ratio_mean"] = float(ratios.mean()); s_sum["discount"] = d_ref
    tor = tornado(cfg, d_ref, ratio); tor.to_csv(out_dir / "tornado.csv", index=False)
    kpi = classification_accuracy(cfg, d_ref, ratio)
    # --- optimiser
    cands = candidate_table(ctx, cfg); cands.to_csv(out_dir / "optimiser_candidates.csv", index=False)
    budget = budget_from(cands, cfg)
    single = optimise_single(cands, budget); single.to_csv(out_dir / "optimiser_single_period.csv", index=False)
    H = cfg["optimiser"]["horizon_weeks"]; mp = cfg["optimiser"]["max_promos_per_week"]
    season = seasonal_index(panel, H)
    cal = optimise_calendar(cands, budget, season, mp); cal.to_csv(out_dir / "promo_plan.csv", index=False)
    dash = dashboard_plan(cands, budget, season, mp, d_ref, "promoted_only")
    rev = dashboard_plan(cands, budget, season, mp, d_ref, "weekly_revenue")
    bsens = []
    for bf in cfg["optimiser"]["budget_sensitivity"]:
        b2 = float(bf * cands.drop_duplicates("family")["weekly_revenue"].sum())
        c2 = optimise_calendar(cands, b2, season, mp)
        bsens.append({"budget_frac": bf, "budget_gbp": b2, **plan_summary(c2, b2), "binding": bool(plan_summary(c2, b2)["subsidy"] > 0.98 * b2)})
    opt = {
        "budget_sensitivity": bsens,
        "n_candidate_families": int(cands["family"].nunique()), "budget_gbp": budget, "horizon_weeks": H, "max_promos_per_week": mp,
        "seasonal_index": [float(x) for x in season],
        "single_period": {**plan_summary(single[single["discount"] > 0], budget), "n_families_discounted": int((single["discount"] > 0).sum()),
                          "discount_counts": {str(k): int(v) for k, v in single["discount"].value_counts().items()}},
        "calendar": plan_summary(cal, budget), "n_families_discounted_calendar": int(cal["family"].nunique()) if len(cal) else 0,
        "dashboard_promoted_only_rank": dash, "top_revenue_rank": rev,
        "plan_within_budget": bool(plan_summary(cal, budget)["subsidy"] <= budget + 1e-6),
    }
    # --- figures
    star = ref.sort_values("family_net").iloc[-1]["stock_code"]; worst = ref.sort_values("family_net").iloc[0]["stock_code"]
    top1 = ref.iloc[0]["stock_code"]
    for tag, s in (("top_revenue_sku", top1), ("best_family_net", star), ("worst_family_net", worst)):
        r = ctx.score(s, d_ref)
        viz.waterfall(r, f"{t.at[s, 'description'][:40]} - {int(d_ref * 100)}% off ({tag.replace('_', ' ')})", fig_dir / f"waterfall_{tag}.png")
    viz.reference_bars(ref, f"Reference promo ({int(d_ref * 100)}% off): promoted-only vs family net", fig_dir / "reference_promo.png")
    viz.tornado_chart(tor, tor.attrs.get("base_net", 0.0), "Tornado: family net swing per assumption", fig_dir / "tornado.png")
    es, xs, z = heatmap_grid(cfg, d_ref, ratio, "substitution_share")
    viz.heatmap(xs, es, z, "substitution share", "elasticity", "Family net: elasticity x substitution", fig_dir / "heatmap_elasticity_substitution.png")
    es, xs, z = heatmap_grid(cfg, d_ref, ratio, "margin")
    viz.heatmap(xs, es, z, "unit margin", "elasticity", "Family net: elasticity x margin", fig_dir / "heatmap_elasticity_margin.png")
    viz.hist(sw["break_even_elasticity"].to_numpy(), "break-even elasticity", "Sweep: break-even elasticity distribution", fig_dir / "breakeven_distribution.png", vline=cfg["demand"]["prior_elasticity"])
    ev = res["elasticities"]
    viz.hist(ev.loc[ev["eligible"], "eps_hat"].to_numpy(), "estimated elasticity (eligible SKUs, before dropping positives)", "Price-response estimates (association, not causal)", fig_dir / "elasticity_estimates.png", vline=0.0, bins=40)
    viz.plan_compare_chart(opt["calendar"]["family_net"], dash["family_net"], rev["family_net"], "8-week plan: true family net by policy", fig_dir / "plan_comparison.png")
    k = 0
    for s in ref_skus:
        if len(ctx.members(s)) > 1 and k < 5:
            r = ctx.score(s, d_ref)
            viz.family_units_chart(r, [t.at[m, "description"] for m in r["members"]], f"{t.at[s, 'family_name'][:35]} @ {int(d_ref * 100)}% off", fig_dir / f"family_units_{k + 1}.png")
            k += 1
    mnl = _mnl_checks(ctx, ref_skus, cfg)
    return {"reference": reference, "reference_sensitivity": sens.to_dict("records"), "sweep": s_sum, "sweep_by_discount": sw_by_d,
            "tornado": tor.to_dict("records"), "tornado_base_net": tor.attrs.get("base_net"), "kpi_classification": kpi,
            "optimiser": opt, "mnl_checks": mnl}


# --------------------------------------------------------------------------- orchestration
def data_summary(raw_rows: int, sales: pd.DataFrame, panel: pd.DataFrame, cfg: dict) -> dict:
    """Headline data numbers and the identifiability report."""
    q4 = sales[sales["invoice_date"].dt.month >= 10]["revenue"].sum() / sales["revenue"].sum()
    return {
        "raw_rows": int(raw_rows), "clean_lines": int(len(sales)), "invoices": int(sales["invoice"].nunique()),
        "skus": int(sales["stock_code"].nunique()), "revenue_gbp": float(sales["revenue"].sum()),
        "date_min": str(sales["invoice_date"].min().date()), "date_max": str(sales["invoice_date"].max().date()),
        "q4_revenue_share": float(q4), "identifiability": price_variation_report(panel, cfg),
    }


def run_pipeline(raw: pd.DataFrame, cfg: dict, out_dir: Path, fig_dir: Path, models_dir: Path | None = None,
                 overrides: str | Path | None = None) -> dict:
    """Run clean -> panel -> engine table -> evaluate and write summary.json / metrics.json."""
    t0 = time.time()
    seed_everything(cfg)
    sales, _ = clean_sales(raw, cfg)
    panel = weekly_panel(sales)
    res = build_engine_table(sales, panel, cfg, overrides)
    save_train_artifacts(res, cfg, out_dir, models_dir)
    summary = {"seed": cfg["seed"], "data": data_summary(len(raw), sales, panel, cfg), **train_summary(res, cfg)}
    summary.update(evaluate(res, panel, cfg, out_dir, fig_dir))
    summary["runtime_seconds"] = round(time.time() - t0, 1)
    summary = to_py(summary)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    metrics = {"identity_tolerance": 1e-6, "sweep_n_draws": summary["sweep"]["n_draws"], **summary["kpi_classification"],
               "pct_promoted_only_profitable": summary["sweep"]["pct_promoted_only_profitable"],
               "pct_family_profitable": summary["sweep"]["pct_family_profitable"],
               "reference_family_net_total_gbp": summary["reference"]["family_net_total_gbp"]}
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return summary


def load_stage_inputs(cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read interim sales/panel parquet written by promo.data."""
    interim = path_for(cfg, "interim")
    return pd.read_parquet(interim / "sales.parquet"), pd.read_parquet(interim / "panel.parquet")


def default_dirs(cfg: dict | None = None) -> tuple[dict, Path, Path, Path]:
    """(cfg, outputs, figures, models) project directories."""
    cfg = cfg or load_config()
    return cfg, path_for(cfg, "outputs", ROOT), path_for(cfg, "figures", ROOT), path_for(cfg, "models", ROOT)
