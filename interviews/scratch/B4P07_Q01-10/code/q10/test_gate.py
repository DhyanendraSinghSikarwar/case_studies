import json, subprocess, sys, pytest
from gate import check, main

CHAMP = {"auc": 0.85, "p95_ms": 40, "size_mb": 90, "slices": {"new_users": 0.78, "mobile": 0.82}, "signature": ["age", "tenure"]}
GOOD = {**CHAMP, "auc": 0.853}

def fails(rows): return [r[0] for r in rows if r[1] == "FAIL"]

def test_pass():
    assert fails(check(GOOD, CHAMP)) == []

def test_regress_vs_champion():
    assert fails(check({**GOOD, "auc": 0.83}, CHAMP)) == ["vs champion auc"]

def test_missing_metric_fails_closed():
    bad = {k: v for k, v in GOOD.items() if k != "p95_ms"}
    assert fails(check(bad, CHAMP)) == ["metrics present"]

def test_no_champion_fails_closed_unless_allowed():
    assert fails(check(GOOD, None)) == ["champion metrics"]
    assert fails(check(GOOD, None, allow_no_champion=True)) == []

def test_slice_regression_is_caught_even_if_overall_ok():
    cand = {**GOOD, "slices": {"new_users": 0.70, "mobile": 0.82}}   # overall fine, one slice dropped
    assert "slice new_users vs champion" in fails(check(cand, CHAMP))

def test_exit_code(tmp_path):
    c, h = tmp_path / "c.json", tmp_path / "h.json"
    h.write_text(json.dumps(CHAMP))
    c.write_text(json.dumps({**GOOD, "auc": 0.83}))
    assert main(["--candidate", str(c), "--champion", str(h)]) == 1
    c.write_text(json.dumps(GOOD))
    assert main(["--candidate", str(c), "--champion", str(h)]) == 0
