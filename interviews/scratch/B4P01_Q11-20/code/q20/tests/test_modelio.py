import joblib
import numpy as np
import pytest
import modelio


def test_save_load_roundtrip(small_df, tmp_path):
    path = tmp_path / "m.joblib"                       # fresh temp dir, auto-cleaned later
    m = modelio.fit_and_save(small_df, path)
    loaded = joblib.load(path)
    np.testing.assert_array_equal(m.predict(small_df[["a", "b"]]), loaded.predict(small_df[["a", "b"]]))


def test_load_embeddings_without_network(monkeypatch):
    monkeypatch.setattr(modelio, "download_pretrained", lambda name: {"fake": name})   # replace the slow call
    assert modelio.load_embeddings("tiny") == {"fake": "tiny"}


@pytest.mark.parametrize("n_rows", [10, 25, 50])
def test_fit_on_subsets(small_df, tmp_path, n_rows):
    modelio.fit_and_save(small_df.head(n_rows), tmp_path / "x.joblib")
    assert (tmp_path / "x.joblib").exists()


@pytest.mark.slow
def test_real_download():
    modelio.load_embeddings("big")                      # would hit the network
