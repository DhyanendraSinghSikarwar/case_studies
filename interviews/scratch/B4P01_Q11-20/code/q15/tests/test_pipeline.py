import numpy as np, pandas as pd
from churn.config import TrainConfig
from churn.pipeline import build_model, split, train, predict


def _df(n=200):
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n), "support_calls": rng.poisson(2, n)})
    df["churned"] = (df.support_calls + rng.normal(0, 1, n) > 2).astype(int)
    return df


def test_scaler_sees_train_rows_only(tmp_path):
    df = _df(); cfg = TrainConfig(data_path="unused")
    Xtr, Xte, ytr, yte = split(df, cfg)
    m = build_model(cfg.seed).fit(Xtr, ytr)
    np.testing.assert_allclose(m["scale"].mean_, Xtr.mean().values)      # train mean
    assert not np.allclose(m["scale"].mean_, df[list(cfg.features)].mean().values)  # NOT the all-rows mean


def test_train_is_deterministic_and_roundtrips(tmp_path):
    p = tmp_path / "d.csv"; _df().to_csv(p, index=False)
    a = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "a.joblib")))
    b = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "b.joblib")))
    assert a == b
    assert len(predict(str(tmp_path / "a.joblib"), _df().head(5))) == 5
