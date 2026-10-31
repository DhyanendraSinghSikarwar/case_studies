from dataclasses import dataclass

@dataclass
class Req:
    human_waiting: bool            # is a person or a blocking system waiting for the answer?
    max_staleness_s: float         # how old may the score be? (0 = must use fresh inputs)
    can_precompute: bool           # is the input space small/known (e.g. all customers)?
    events_per_s: float = 0.0      # continuous event stream volume (0 = none)
    latency_budget_ms: float = 0.0 # only meaningful for human_waiting

def pick_mode(r: Req) -> str:
    if r.max_staleness_s < 0 or r.events_per_s < 0:
        raise ValueError("negative input")
    if r.human_waiting:
        if r.max_staleness_s >= 3600 and r.can_precompute:
            return "batch+kv"                     # precompute, serve lookup (hybrid)
        return "online"
    if r.events_per_s > 0:
        return "streaming" if r.max_staleness_s < 60 else "micro-batch"
    return "batch"
