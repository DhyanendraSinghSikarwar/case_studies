import pytest
from pick_mode import Req, pick_mode

@pytest.mark.parametrize("req,expected", [
    (Req(False, 86400, True),                 "batch"),        # nightly churn scores
    (Req(True, 0, False, latency_budget_ms=100), "online"),    # fraud check at checkout
    (Req(False, 5, False, events_per_s=2000), "streaming"),    # per-event anomaly scoring
    (Req(False, 300, False, events_per_s=2000), "micro-batch"),# 5-minute freshness is enough
    (Req(True, 86400, True),                  "batch+kv"),     # "recommended for you" page
    (Req(True, 86400, False),                 "online"),       # cannot precompute -> must compute live
])
def test_modes(req, expected):
    assert pick_mode(req) == expected

def test_bad_input():
    with pytest.raises(ValueError):
        pick_mode(Req(True, -1, False))
