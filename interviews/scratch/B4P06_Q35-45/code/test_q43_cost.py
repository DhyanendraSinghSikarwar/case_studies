import sys, pathlib, math; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q43_cost import *
CPU = Realtime(1.0, 50, 0.6); B = Batch(1.0, 400, 0.4)

def test_replicas_hand_check():             # 80 rps / (50*0.6=30 per replica) = 2.67 -> 3
    assert replicas_needed(80, CPU) == 3
def test_min_replicas_floor():
    assert replicas_needed(1, Realtime(1, 50, 0.6, min_replicas=2)) == 2
def test_static_cost():                     # 3 replicas * 1.0 * 24
    assert realtime_static_cost_per_day(20, 4, CPU) == (72.0, 3)
def test_autoscaled_cheaper_than_static():
    assert realtime_autoscaled_cost_per_day(20, CPU)[0] < realtime_static_cost_per_day(20, 4, CPU)[0]
def test_batch_hand_check():                # 1,728,000 preds / (400*3600=1.44M per h) = 1.2 h + 0.25 = 1.45 h * 0.4
    assert math.isclose(batch_cost_per_day(1_728_000, B), 1.45 * 0.4)
def test_per_1000():
    assert per_1000(72.0, 1_728_000) == 72.0 * 1000 / 1_728_000
def test_breakeven_runs_hand_check():       # one run = 1.45 h * 0.4 = 0.58 cu; 24 / 0.58 = 41.38 runs
    assert math.isclose(breakeven_runs_per_day(24.0, 1_728_000, B), 24.0 / 0.58)
def test_breakeven_is_where_costs_cross():
    r = breakeven_runs_per_day(24.0, 1_728_000, B)
    assert math.isclose(r * batch_cost_per_day(1_728_000, B), 24.0)
    assert 24 * batch_cost_per_day(1_728_000, B) < 24.0       # hourly batch is still cheaper here
def test_low_utilisation_costs_more_per_prediction():
    c1 = per_1000(24.0, 100_000); c2 = per_1000(24.0, 1_000_000); assert c1 == 10 * c2
