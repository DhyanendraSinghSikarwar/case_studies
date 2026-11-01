"""Promotion state machine: staging -> shadow -> canary5 -> full. Aborts on bad metrics."""
from dataclasses import dataclass

STAGES = ["staging", "shadow", "canary5", "full"]


@dataclass(frozen=True)
class Criteria:
    max_error_rate: float = 0.01
    max_p99_ms: float = 250.0
    max_psi: float = 0.2          # prediction distribution shift versus champion
    min_requests: int = 1000      # do not judge on fewer


def judge(stage, m, c=Criteria()):
    """Return ('advance'|'wait'|'abort', reason) for one stage's metrics."""
    if stage == "staging":  # smoke test: pass/fail only
        return ("advance", "smoke ok") if m["smoke_passed"] else ("abort", "smoke test failed")
    if m["requests"] < c.min_requests:
        return "wait", f"only {m['requests']} requests (< {c.min_requests})"
    if m["error_rate"] > c.max_error_rate:
        return "abort", f"error rate {m['error_rate']:.3f} > {c.max_error_rate}"
    if m["p99_ms"] > c.max_p99_ms:
        return "abort", f"p99 {m['p99_ms']}ms > {c.max_p99_ms}ms"
    if m["psi"] > c.max_psi:
        return "abort", f"prediction PSI {m['psi']} > {c.max_psi}"
    return "advance", "metrics within limits"


class Promotion:
    def __init__(self):
        self.stage, self.state, self.log = "staging", "running", []

    def step(self, metrics):
        if self.state != "running":
            raise RuntimeError(f"promotion already {self.state}")
        verdict, why = judge(self.stage, metrics)
        self.log.append((self.stage, verdict, why))
        if verdict == "abort":
            self.state = "aborted"  # traffic goes back to champion (done by the router/rollout tool)
        elif verdict == "advance":
            self.stage = STAGES[STAGES.index(self.stage) + 1]
            if self.stage == "full":
                self.state = "done"  # 100% traffic reached; keep watching with normal monitoring
        return verdict
