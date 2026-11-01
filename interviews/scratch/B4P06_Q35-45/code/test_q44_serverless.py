import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dataclasses import replace
from q44_serverless import Workload, choose
BASE = Workload(model_mb=50, needs_gpu=False, avg_rps=0.5, peak_to_avg=10, p99_budget_ms=2000, cold_start_ms=600, idle_fraction=0.7)

def test_small_spiky_model_fits_function(): assert choose(BASE)[0] == "serverless function"
def test_gpu_never_serverless(): assert choose(replace(BASE, needs_gpu=True))[0].startswith("managed endpoint (GPU)")
def test_steady_heavy_traffic_goes_always_on(): assert "always-on" in choose(replace(BASE, avg_rps=50))[0]
def test_strict_p99_with_slow_cold_start_keeps_warm(): assert "min instances" in choose(replace(BASE, p99_budget_ms=500, cold_start_ms=600))[0]
def test_medium_model_container_scale_to_zero(): assert choose(replace(BASE, model_mb=900))[0] == "serverless container (scale to zero)"
def test_huge_model_always_on(): assert "always-on" in choose(replace(BASE, model_mb=8000))[0]
def test_reasons_are_returned(): assert all(len(choose(w)[1]) >= 1 for w in [BASE, replace(BASE, needs_gpu=True), replace(BASE, avg_rps=50)])
