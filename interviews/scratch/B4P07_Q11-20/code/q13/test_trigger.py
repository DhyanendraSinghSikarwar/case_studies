import datetime as dt
from trigger import decide

NOW = dt.datetime(2026, 10, 26, 12, tzinfo=dt.timezone.utc)
def ago(h): return NOW - dt.timedelta(hours=h)

def test_schedule_with_data():
    assert decide("schedule", 9000, ago(100), NOW, 0)[0] is True

def test_schedule_too_little_data():
    go, why = decide("schedule", 100, ago(100), NOW, 0)
    assert not go and "new rows" in why

def test_cooldown_blocks_noisy_alert():
    go, why = decide("repository_dispatch", 9000, ago(2), NOW, 1, drift_alert=True)
    assert not go and "cooldown" in why

def test_alert_after_cooldown():
    assert decide("repository_dispatch", 9000, ago(30), NOW, 1, drift_alert=True)[0]

def test_cost_cap_beats_manual():
    go, why = decide("workflow_dispatch", 0, ago(1), NOW, 3)
    assert not go and "cost cap" in why

def test_manual_ignores_cooldown():
    assert decide("workflow_dispatch", 0, ago(1), NOW, 0)[0]

def test_push_never_retrains():
    assert not decide("push", 99999, None, NOW, 0)[0]

def test_first_ever_run_has_no_cooldown():
    assert decide("schedule", 9000, None, NOW, 0)[0]
