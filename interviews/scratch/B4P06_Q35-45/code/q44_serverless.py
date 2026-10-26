"""Rule-based picker: serverless function / serverless container / managed endpoint / always-on cluster.
Thresholds are INVENTED teaching defaults, not cloud limits. Check current provider docs for real limits."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Workload:
    model_mb: float            # size of model plus runtime image
    needs_gpu: bool
    avg_rps: float
    peak_to_avg: float         # burstiness
    p99_budget_ms: float       # strict latency need
    cold_start_ms: float       # your measured cold start for this image (measure it)
    idle_fraction: float       # share of the day with no traffic, 0..1
    team_runs_k8s: bool = False

FUNCTION_MAX_MB = 250          # invented stand-in for a function package/image ceiling; real ceilings differ per provider, check docs
CONTAINER_MAX_MB = 4000        # invented stand-in for a comfortable serverless-container image size
STEADY_RPS = 5                 # above this average, always-on capacity is usually cheaper than per-request billing (invented)

def choose(w: Workload) -> tuple[str, list[str]]:
    why = []
    if w.needs_gpu:
        why.append("GPU needed: many serverless options have no GPU or a limited one (check current docs)")
        return ("managed endpoint (GPU) or cluster", why)
    cold_ok = w.cold_start_ms <= w.p99_budget_ms * 0.5
    if not cold_ok and w.idle_fraction > 0:
        why.append(f"cold start {w.cold_start_ms:.0f} ms is over half the p99 budget: scale-to-zero would breach it; keep min instances warm")
    if w.avg_rps >= STEADY_RPS:
        why.append(f"avg {w.avg_rps} rps is steady and heavy: always-on capacity usually beats per-request billing")
        return ("managed endpoint or cluster (always-on)", why)
    if w.model_mb > CONTAINER_MAX_MB:
        why.append("large model: image pull and load make cold starts long; prefer warm replicas")
        return ("managed endpoint or cluster (always-on)", why)
    if w.model_mb <= FUNCTION_MAX_MB and cold_ok:
        why.append("small model, low traffic, cold start fits the budget: a function fits")
        return ("serverless function", why)
    if not cold_ok:
        why.append("serverless container with minimum instances > 0 (pays for idle, kills cold start)")
        return ("serverless container (min instances > 0)", why)
    why.append("model too big for a function package but fine for a container image; low traffic favours scale to zero")
    return ("serverless container (scale to zero)", why)
