import pytest

from rollout import Promotion, judge

OK = {"requests": 5000, "error_rate": 0.002, "p99_ms": 120, "psi": 0.05}


def run(seq):
    p = Promotion()
    for m in seq:
        p.step(m)
    return p


def test_happy_path_reaches_full():
    p = run([{"smoke_passed": True}, OK, OK])
    assert (p.stage, p.state) == ("full", "done")


def test_smoke_failure_aborts_at_staging():
    p = run([{"smoke_passed": False}])
    assert (p.stage, p.state) == ("staging", "aborted")


def test_too_few_requests_waits_not_advances():
    p = Promotion(); p.step({"smoke_passed": True})
    assert p.step({**OK, "requests": 50}) == "wait"
    assert p.stage == "shadow" and p.state == "running"


@pytest.mark.parametrize("bad,key", [({"error_rate": 0.05}, "error"), ({"p99_ms": 900}, "p99"), ({"psi": 0.4}, "PSI")])
def test_each_abort_criterion(bad, key):
    v, why = judge("canary5", {**OK, **bad})
    assert v == "abort" and key in why


def test_cannot_step_after_abort():
    p = run([{"smoke_passed": False}])
    with pytest.raises(RuntimeError):
        p.step(OK)


def test_low_volume_bad_metrics_is_not_judged():
    assert judge("canary5", {**OK, "requests": 10, "error_rate": 0.5})[0] == "wait"
