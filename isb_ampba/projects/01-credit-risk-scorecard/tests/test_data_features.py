from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from credit.data import PAY_COLS, TARGET, clean, make_fixture, split
from credit.features import ENGINEERED, add_features, feature_cols
from credit.validate import validate_raw


def test_clean_maps_education_and_marriage(raw):
    out = clean(raw)
    assert set(out["EDUCATION"].unique()) <= {1, 2, 3, 4}
    assert set(out["MARRIAGE"].unique()) <= {1, 2, 3}
    assert len(out) == len(raw)


def test_split_is_stratified_and_disjoint(raw, cfg):
    df = clean(raw)
    tr, va, te = split(df, cfg)
    idx = [set(d.index) for d in (tr, va, te)]
    assert not (idx[0] & idx[1]) and not (idx[0] & idx[2]) and not (idx[1] & idx[2])
    assert set().union(*idx) == set(df.index)
    for d in (tr, va, te):
        assert abs(d[TARGET].mean() - df[TARGET].mean()) < 0.01


def test_validate_rejects_bad_target(raw):
    assert validate_raw(raw, expected_rows=None)["rows"] == len(raw)
    bad = raw.copy()
    bad.loc[bad.index[0], TARGET] = 2
    with pytest.raises(AssertionError):
        validate_raw(bad, expected_rows=None)


def test_make_fixture_is_valid_and_reproducible():
    a, b = make_fixture(300, seed=1), make_fixture(300, seed=1)
    assert a.equals(b)
    assert validate_raw(a, expected_rows=300)["default_rate"] > 0
    assert not np.isnan(a.to_numpy()).any()


def test_utilisation_identity(raw):
    f = add_features(raw)
    assert np.allclose(f["util_1"] * f["LIMIT_BAL"], f["BILL_AMT1"])


def test_pay_ratio_bounds_and_delay_trend(raw):
    f = add_features(raw)
    for i in range(1, 6):
        assert f[f"pay_ratio_{i}"].between(0, 1).all()
    row = pd.DataFrame([raw.iloc[0]])
    # delays oldest->newest [0,0,0,1,2,3]; PAY_6 is oldest, PAY_0 newest
    for c, v in zip(PAY_COLS[::-1], [0, 0, 0, 1, 2, 3], strict=True):
        row[c] = v
    assert add_features(row)["delay_trend"].iloc[0] > 0


def test_no_target_leakage(raw, cfg):
    f = add_features(raw)
    cols = feature_cols(f, cfg)
    assert TARGET not in cols and "SEX" not in cols
    for c in ENGINEERED:
        assert abs(np.corrcoef(f[c], f[TARGET])[0, 1]) < 0.99
