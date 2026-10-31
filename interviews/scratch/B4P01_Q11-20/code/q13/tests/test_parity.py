import importlib, os
import numpy as np, pandas as pd, pytest

IMPL = os.environ.get("SERVICE", "shared")


def test_serving_matches_golden_training_features():
    raw = pd.read_csv("golden_raw.csv")
    want = pd.read_csv("golden_features.csv").values
    rows = [{k: (None if v != v else v) for k, v in r.items()} for r in raw.to_dict("records")]
    got = np.array(importlib.import_module(f"service_{IMPL}").predict_features(rows), dtype=float)
    assert got.shape == want.shape
    bad = np.where(~np.isclose(got, want, rtol=0, atol=1e-6))
    assert bad[0].size == 0, f"{len(set(bad[0]))} of {len(want)} rows differ; first: row {bad[0][0]} col {bad[1][0]} got {got[bad[0][0], bad[1][0]]} want {want[bad[0][0], bad[1][0]]}"


def test_schema_contract_rejects_bad_payload():
    from features import RawRow
    with pytest.raises(Exception):
        RawRow(age="old", household=2)
