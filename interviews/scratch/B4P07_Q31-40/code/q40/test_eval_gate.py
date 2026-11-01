import json
from eval_gate import run_gate, deterministic_checks, stub_model, stub_judge

CASES = [json.loads(l) for l in open("golden.jsonl")]

def test_good_stub_passes():
    summary, problems = run_gate(CASES)
    assert problems == []
    assert summary["notes"]            # a noisy case was seen, but the rate stayed above 0.9

def test_single_runs_are_noisier_than_the_tolerance_so_we_average():
    summary, problems = run_gate(CASES)
    assert summary["judge_spread"] > 0.3          # one run could trip a 0.3 tolerance by luck
    assert abs(summary["judge_mean"] - 4.4) < 0.3  # the mean over repeats stays inside it

def test_broken_format_fails_deterministic_gate():
    bad = lambda p, s: "plain text, not json"
    summary, problems = run_gate(CASES, model=bad)
    assert any("deterministic pass rate" in p for p in problems)

def test_banned_phrase_is_caught():
    case = CASES[0]
    raw = json.dumps({"answer": "Refund: ignore previous instructions", "source": "x"})
    assert any("banned" in f for f in deterministic_checks(case, raw))

def test_quality_drop_beyond_tolerance_fails():
    worse = lambda p, o, s: 3.5
    _, problems = run_gate(CASES, judge=worse)
    assert any("floor" in p for p in problems) and any("tolerance" in p for p in problems)
