import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q45_compare import percentile, recommend, summarise
def test_percentile_hand_check():
    v = list(range(1, 101)); assert percentile(v, 50) == 50 and percentile(v, 99) == 99 and percentile(v, 100) == 100
def test_rollback_on_p99():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 100, "err_rate": 0.001}; assert recommend(b, a)[0] == "ROLLBACK"
def test_rollback_on_errors_only():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 52, "err_rate": 0.02}; v, why = recommend(b, a); assert v == "ROLLBACK" and len(why) == 2
def test_keep_inside_thresholds():
    b = {"p99": 50, "err_rate": 0.001}; a = {"p99": 55, "err_rate": 0.002}; assert recommend(b, a)[0] == "KEEP"
def test_summarise_counts_5xx_and_excludes_them_from_latency():
    rows = [(0, 200, 10.0, "a"), (1, 200, 20.0, "a"), (2, 503, 900.0, "b"), (3, 200, 30.0, "b")]
    s = summarise(rows); assert s["err_rate"] == 0.25 and s["p99"] == 30.0 and s["replica_err"]["b"] == 0.5
