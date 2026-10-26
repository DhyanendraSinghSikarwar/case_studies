import inspect, numpy as np, pytest
from sklearn.linear_model import LogisticRegression
from llm_train import make_data, train

def test_no_leakage_on_pure_noise():
    # labels are coin flips, so any honest pipeline scores ~0.5. Averaging over 10 datasets removes luck.
    accs = [train(*make_data(s), "/tmp/_m.joblib")[1] for s in range(10)]
    assert np.mean(accs) < 0.65, f"mean accuracy {np.mean(accs):.2f} on noise labels = leakage"

def test_same_input_same_result():
    X, y = make_data()
    a = train(X, y, "/tmp/_m.joblib")[1]
    b = train(X, y, "/tmp/_m.joblib")[1]
    assert a == b, f"two runs differ ({a:.3f} vs {b:.3f}): no seed"

def test_model_file_really_written(tmp_path):
    X, y = make_data()
    train(X, y, str(tmp_path / "missing_dir" / "m.joblib"))     # directory does not exist
    assert (tmp_path / "missing_dir" / "m.joblib").exists(), "save failed silently"

def test_invented_parameters_do_not_exist():
    # check the claim against the installed library, never against the LLM's confidence
    params = inspect.signature(LogisticRegression).parameters
    assert "class_weight" in params and "class_weights" not in params
