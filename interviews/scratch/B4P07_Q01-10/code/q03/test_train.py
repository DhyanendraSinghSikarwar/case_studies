import math, pytest, joblib, numpy as np
from train_lib import make_data, train

def test_smoke_train(tmp_path):
    X, y = make_data(300)                       # a few hundred rows
    out = tmp_path / "model.joblib"
    losses = train(X, y, epochs=2, out_path=out)
    assert all(math.isfinite(v) for v in losses)     # no NaN / inf
    assert losses[-1] < losses[0]                    # loss falls
    assert out.exists() and out.stat().st_size > 0   # artifact written
    clf = joblib.load(out)                           # artifact reloads
    assert clf.predict(X[:5]).shape == (5,)

@pytest.mark.slow
def test_full_train_quality(tmp_path):
    X, y = make_data(20000, seed=1)
    losses = train(X, y, epochs=50, out_path=tmp_path / "m.joblib")
    clf = joblib.load(tmp_path / "m.joblib")
    assert (clf.predict(X) == y).mean() > 0.75       # nightly quality floor
