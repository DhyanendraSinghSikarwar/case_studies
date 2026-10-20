"""Shared offline fixtures: real-data sample (CSV, 1,500 rows) and a fitted scorecard."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from credit import scorecard as sc  # noqa: E402
from credit import woe  # noqa: E402
from credit.config import load_config  # noqa: E402
from credit.data import TARGET, clean, split  # noqa: E402
from credit.features import add_features, feature_cols  # noqa: E402


@pytest.fixture(scope="session")
def cfg() -> dict:
    return load_config()


@pytest.fixture(scope="session")
def raw() -> pd.DataFrame:
    return pd.read_csv(ROOT / "tests" / "fixtures" / "uci350_sample.csv")


@pytest.fixture(scope="session")
def splits(raw, cfg):
    tr, va, te = split(clean(raw), cfg)
    return add_features(tr), add_features(va), add_features(te)


@pytest.fixture(scope="session")
def fitted(splits, cfg):
    """Binning process + WOE logistic scorecard fitted on the fixture train split."""
    tr, _, _ = splits
    cols = feature_cols(tr, cfg)
    bp = woe.fit_binning(tr[cols], tr[TARGET], cfg["scorecard"]["iv_min"], cfg["seed"])
    iv = woe.iv_table(bp).set_index("name")["iv"]
    lr, sc_cols = sc.fit_logit_scorecard(woe.woe_transform(bp, tr[cols]), tr[TARGET], iv,
                                         cfg["scorecard"]["corr_max"])
    table = sc.build_points_table(bp, lr, sc_cols, cfg["scorecard"])
    return {"bp": bp, "lr": lr, "cols": sc_cols, "table": table, "features": cols, "iv": iv}
