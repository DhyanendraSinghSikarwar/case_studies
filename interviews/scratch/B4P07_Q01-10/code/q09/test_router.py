from router import route

def test_docs_only_runs_nothing():
    assert route(["README.md", "docs/setup.md"]) == []

def test_code_only_change():
    assert route(["src/features.py", "tests/test_features.py"]) == ["code_ci"]

def test_serving_change_rebuilds_image():
    assert route(["src/serving/app.py"]) == ["code_ci", "serving_rebuild"]

def test_model_only_change_does_not_rebuild_image():
    r = route(["configs/train_churn.yaml"])
    assert "model_ct" in r and "serving_rebuild" not in r

def test_data_pointer_triggers_training_only():
    assert route(["data/train.csv.dvc"]) == ["model_ct"]

def test_alias_move_is_pointer_only():
    assert route(["deploy/alias.yaml"]) == ["promote_pointer"]

def test_dependency_bump_hits_everything():
    assert route(["requirements.txt"]) == ["code_ci", "model_ct", "serving_rebuild"]

def test_unknown_path_fails_safe():
    assert route(["weird/thing.bin"]) == ["code_ci"]

def test_mixed_change_unions():
    assert route(["src/training/loss.py", "src/serving/app.py"]) == ["code_ci", "model_ct", "serving_rebuild"]
