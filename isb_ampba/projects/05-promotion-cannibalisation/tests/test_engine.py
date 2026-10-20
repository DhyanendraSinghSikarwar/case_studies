import numpy as np

from promo.engine import break_even_elasticity, reference_promo, score_promo


def _rand_case(rng):
    n = int(rng.integers(1, 7))
    u = rng.uniform(1, 500, n)
    p = rng.uniform(0.5, 20, n)
    return (u, p, int(rng.integers(0, n)), float(rng.uniform(0, 0.5)), float(rng.uniform(-8, -0.5)), float(rng.uniform(0.2, 0.6)),
            float(rng.uniform(0, 3)), float(rng.uniform(0, 10)), float(rng.uniform(0.0, 1.0)))


def test_engine_identity(cfg):
    rng = np.random.default_rng(42)
    for _ in range(300):
        u, p, i, d, eps, m, hu, hm, sw = _rand_case(rng)
        r = score_promo(u, p, i, d, eps, m, hu, hm, cfg, sub_weight=sw)
        assert abs(r["family_net"] - (r["direct_uplift"] - r["subsidy_cost"] - r["cannibalised_margin"] + r["halo_margin"])) < 1e-6
        assert abs(r["promoted_only"] - (r["direct_uplift"] - r["subsidy_cost"])) < 1e-9
        assert abs(r["subsidy_cost"] - d * p[i] * u[i] * cfg["engine"]["promo_weeks"]) < 1e-9


def test_no_promo_zero_effect(cfg, family):
    u, p = family
    r = score_promo(u, p, 0, 0.0, -2.5, 0.4, 1.0, 1.0, cfg)
    for k in ("direct_uplift", "subsidy_cost", "cannibalised_margin", "halo_margin", "family_net", "promoted_only", "incremental_units"):
        assert abs(r[k]) < 1e-9


def test_cannibalised_nonnegative(cfg):
    rng = np.random.default_rng(1)
    for _ in range(200):
        u, p, i, d, eps, m, hu, hm, sw = _rand_case(rng)
        assert score_promo(u, p, i, d, eps, m, hu, hm, cfg, sub_weight=sw)["cannibalised_margin"] >= 0


def test_promoted_only_ignores_siblings(cfg, family):
    u, p = family
    a = score_promo(u, p, 0, 0.1, -3.0, 0.4, 0.0, 0.0, cfg)
    b = score_promo(u, p * np.array([1.0, 1.5, 0.7]), 0, 0.1, -3.0, 0.4, 0.0, 0.0, cfg)
    assert abs(a["promoted_only"] - b["promoted_only"]) < 1e-9      # promoted-only depends on the promoted SKU alone
    assert abs(a["family_net"] - b["family_net"]) > 1e-6            # the family view reacts to sibling prices


def test_break_even_root(cfg, family):
    u, p = family
    be = break_even_elasticity(u, p, 0, 0.10, 0.4, 1.0, 0.5, cfg)
    assert np.isfinite(be)
    r = score_promo(u, p, 0, 0.10, be, 0.4, 1.0, 0.5, cfg)
    assert abs(r["family_net"]) < 1e-5


def test_break_even_nan_when_never_pays(cfg, family):
    u, p = family
    assert np.isnan(break_even_elasticity(u, p, 0, 0.25, 0.05, 0.0, 0.0, cfg))   # margin 5% < discount: never pays
    assert np.isnan(break_even_elasticity(u, p, 0, 0.0, 0.4, 0.0, 0.0, cfg))


def test_more_elastic_means_more_net(cfg, family):
    u, p = family
    nets = [score_promo(u, p, 0, 0.1, e, 0.4, 0.5, 0.3, cfg)["family_net"] for e in (-1, -2, -4, -8)]
    assert all(a < b for a, b in zip(nets, nets[1:]))


def test_context_reference_promo(ctx):
    skus = list(ctx.table[ctx.table["active"]].index[:5])
    ref = reference_promo(ctx, skus, 0.10)
    assert len(ref) == 5
    assert np.allclose(ref["family_net"], ref["direct_uplift"] - ref["subsidy_cost"] - ref["cannibalised_margin"] + ref["halo_margin"], atol=1e-6)
