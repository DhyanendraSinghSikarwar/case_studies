import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from churn import FEATURES, add_ratio, make_data, train


# 1. UNIT: one small function, hand-checkable, runs in milliseconds
@pytest.mark.unit
def test_add_ratio_zero_tenure_does_not_divide_by_zero():
    out = add_ratio(pd.DataFrame({"monthly_spend": [50.0], "tenure_months": [0]}))
    assert out.spend_per_month_tenure.iloc[0] == 50.0


# 2. DATA: schema, ranges, nulls, label balance (this is what catches silent data change)
@pytest.mark.data
def test_schema_ranges_and_nulls(df):
    assert list(df.columns) == FEATURES + ["churned"]
    assert df[FEATURES].notna().all().all()
    assert df.tenure_months.between(1, 72).all() and (df.support_calls >= 0).all()
    assert 0.05 < df.churned.mean() < 0.95          # not all one class


@pytest.mark.data
def test_spend_unit_did_not_change(df):
    # catches a silent unit change (e.g. rupees -> paise) that no Python error would ever flag
    assert 30 < df.monthly_spend.mean() < 90


# 3. MODEL: behaviour after training (needs a fit, so slower)
@pytest.mark.model
def test_beats_baseline_and_is_directional(df):
    tr, te = train_test_split(df, test_size=0.25, random_state=0, stratify=df.churned)
    model = train(tr)
    auc = roc_auc_score(te.churned, model.predict_proba(te[FEATURES])[:, 1])
    assert auc > 0.6                                  # floor chosen by the team, not a universal number
    low, high = te.iloc[[0]].copy(), te.iloc[[0]].copy()
    low["support_calls"], high["support_calls"] = 0, 8
    assert model.predict_proba(high[FEATURES])[0, 1] > model.predict_proba(low[FEATURES])[0, 1]


@pytest.mark.model
def test_same_seed_same_predictions(df):
    p1 = train(df, seed=1).predict_proba(df[FEATURES])
    p2 = train(df, seed=1).predict_proba(df[FEATURES])
    np.testing.assert_allclose(p1, p2)


# 4. INTEGRATION: the whole path, raw data to saved model to predictions for new rows
@pytest.mark.integration
def test_end_to_end_with_save_and_load(tmp_path):
    import joblib
    data = make_data(seed=3)
    joblib.dump(train(data), tmp_path / "m.joblib")
    loaded = joblib.load(tmp_path / "m.joblib")
    new_rows = pd.DataFrame({"tenure_months": [3], "monthly_spend": [80.0], "support_calls": [5]})
    p = loaded.predict_proba(new_rows[FEATURES])[0, 1]
    assert 0.0 <= p <= 1.0
