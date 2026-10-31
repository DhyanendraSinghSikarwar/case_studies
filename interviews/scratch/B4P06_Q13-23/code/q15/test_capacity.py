import pytest
from capacity import replicas, survives_zone_loss
def test_hand_example():
    # invented inputs: 800 rps target, one replica sustains 100 rps at p99 target, plan 60%, +1 spare
    assert replicas(800, 100, 0.6, 1) == 15            # 800 / 60 = 13.33 -> 14, +1 = 15
def test_no_headroom_is_smaller():
    assert replicas(800, 100, 1.0, 0) == 8
def test_batching_changes_the_input_not_the_formula():
    assert replicas(800, 250, 0.6, 1) == 7             # 800 / 150 = 5.33 -> 6, +1
def test_zone_loss():
    assert survives_zone_loss(15, 3, 800, 100, 1.0)    # lose 5, 10 left = 1000 rps >= 800
    assert not survives_zone_loss(9, 3, 800, 100, 1.0) # lose 3, 6 left = 600 < 800
@pytest.mark.parametrize("bad", [(0, 100), (800, 0)])
def test_bad_input(bad):
    with pytest.raises(ValueError): replicas(*bad)
