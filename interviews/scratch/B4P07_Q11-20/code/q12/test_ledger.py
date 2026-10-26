import pytest, ledger


def test_promote_then_rollback(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci")
    ledger.promote(f, 2, "ci")
    assert ledger.current(f) == "2"
    r = ledger.rollback(f, "asha", "auc drop in prod")
    assert r["to"] == "1" and r["from"] == "2"
    assert ledger.current(f) == "1"
    assert len(ledger.read(f)) == 3          # history kept, nothing deleted


def test_rollback_needs_reason(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    with pytest.raises(ValueError):
        ledger.rollback(f, "asha", "  ")


def test_nothing_to_roll_back(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci")
    with pytest.raises(RuntimeError):
        ledger.rollback(f, "asha", "oops")


def test_missing_artifact_refuses(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    with pytest.raises(RuntimeError, match="no longer exists"):
        ledger.rollback(f, "asha", "bad", exists=lambda v: False)
    assert ledger.current(f) == "2"          # failed rollback changes nothing


def test_second_rollback_goes_forward_again(tmp_path):
    # after 1,2 then rollback to 1, a second rollback returns to 2 (last different version)
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    ledger.rollback(f, "a", "x")
    r = ledger.rollback(f, "a", "undo")
    assert r["to"] == "2"


def test_explicit_target(tmp_path):
    f = tmp_path / "l.jsonl"
    for v in (1, 2, 3):
        ledger.promote(f, v, "ci")
    r = ledger.rollback(f, "a", "skip 2, it is bad too", target=1)
    assert r["to"] == "1" and ledger.current(f) == "1"
