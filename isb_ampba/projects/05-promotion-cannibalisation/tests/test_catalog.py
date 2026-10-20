import pandas as pd

from promo.baskets import mine_rules
from promo.catalog import apply_overrides, build_families, clean_description, copurchase_share, substitution_weights
from promo.data import FIXTURE_FAMILIES, sku_descriptions


def _fam(sales_panel, cfg):
    return build_families(sku_descriptions(sales_panel[0]), cfg)


def test_clean_description_drops_colours_and_digits(cfg):
    assert clean_description("RED 12 LUNCH BAG", cfg["families"]["drop_words"]) == "lunch bag"


def test_families_cover_every_sku_once(sales_panel, cfg):
    fam = _fam(sales_panel, cfg)
    assert fam["stock_code"].is_unique
    assert set(fam["stock_code"]) == set(sales_panel[0]["stock_code"])
    assert (fam["n_members"] == fam.groupby("family")["stock_code"].transform("size")).all()


def test_variants_cluster_into_one_family(sales_panel, cfg):
    fam = _fam(sales_panel, cfg)
    for name in FIXTURE_FAMILIES:
        ids = fam[fam["description"].str.endswith(name)]["family"]
        assert ids.nunique() == 1 and len(ids) == 4


def test_family_override_applied(sales_panel, cfg, tmp_path):
    fam = _fam(sales_panel, cfg)
    target = fam.loc[fam["description"].str.endswith("MUG"), "family"].iloc[0]
    sku = fam.loc[fam["description"].str.endswith("LUNCH BAG"), "stock_code"].iloc[0]
    csv = tmp_path / "ov.csv"
    pd.DataFrame({"stock_code": [sku], "family": [target]}).to_csv(csv, index=False)
    out = apply_overrides(fam, csv)
    assert out.set_index("stock_code").at[sku, "family"] == target
    assert out["stock_code"].is_unique


def test_copurchase_share_bounds_and_weights(sales_panel, cfg):
    fam = _fam(sales_panel, cfg)
    cop = copurchase_share(sales_panel[0], fam, cfg)
    assert len(cop) == 5 and cop["copurchase_share"].between(0, 1).all()
    cfg2 = {**cfg, "families": {**cfg["families"], "copurchase_weak_threshold": 0.0}}
    cop2 = copurchase_share(sales_panel[0], fam, cfg2)
    w = substitution_weights(fam, cop2, cfg2)
    assert (w.loc[w["n_members"] > 1, "sub_weight"] == cfg["families"]["weak_sub_weight"]).all()


def test_halo_rule_found_and_same_family_excluded(engine_res):
    rules = engine_res["rules"]
    assert ((rules["antecedent"] == "20000") & (rules["consequent"] == "30000")).any()
    fam_of = dict(zip(engine_res["families"]["stock_code"], engine_res["families"]["family"]))
    assert (rules["antecedent"].map(fam_of) != rules["consequent"].map(fam_of)).all()


def test_mine_rules_empty_basket(cfg):
    assert mine_rules(pd.DataFrame(), {}, cfg).empty
