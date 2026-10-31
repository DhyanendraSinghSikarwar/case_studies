import numpy as np, pytest
from monitors import MONITORS, clean_batch, inject

# expected: which monitors MUST fire for each fault (the rest are not asserted here; the matrix script reports them)
MUST = {"null_spike": {"null"}, "unit_change": {"drift", "range"}, "mean_shift": {"drift"}, "dropped_partition": {"category"}}
SEEDS = range(30)

@pytest.mark.parametrize("fault", list(MUST))
def test_fault_detected(fault):
    hits = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(1000 + s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): hits[m] += bool(f(ref, cur))
    for m in MUST[fault]:
        assert hits[m] / len(SEEDS) >= 0.95, (fault, m, hits)

def test_clean_batches_are_quiet():
    fa = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        ref, cur = clean_batch(rng), clean_batch(rng)
        for m, f in MONITORS.items(): fa[m] += bool(f(ref, cur))
    assert all(v / len(SEEDS) <= 0.05 for v in fa.values()), fa

def test_null_spike_does_not_trigger_volume():
    rng = np.random.default_rng(7)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "null_spike", rng)
    assert not MONITORS["volume"](ref, cur)

def test_volume_monitor_misses_a_one_in_four_drop():
    """Documented limit found by the first run: dropping 1 of 4 regions leaves 75 percent of rows, above the 0.7 floor."""
    rng = np.random.default_rng(9)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "dropped_partition", rng)
    assert not MONITORS["volume"](ref, cur)
    assert MONITORS["category"](ref, cur)
