# Plain-assert tests over a MOCK agent: budget invariant, forbidden-tool invariant, replay determinism, plus a repeated-run threshold.
# The "LLM" is a scripted policy with a seeded wobble; tools are mocked with fixtures. No network.
import json, random

FIXTURES = {("search", "pune weather"): "31C sunny", ("search", "mumbai weather"): "29C rain"}   # deterministic mock tool results
FORBIDDEN = {"delete_account"}

class MockLLM:
    """Scripted policy. `wobble` simulates non-determinism: with prob wobble it skips a useful step."""
    def __init__(self, seed, wobble=0.0, bad_tool=False): self.rng, self.wobble, self.bad = random.Random(seed), wobble, bad_tool
    def next(self, state):
        if self.bad and state["steps"] == 0: return ("tool", "delete_account", "user1")
        if not state["obs"] and self.rng.random() >= self.wobble: return ("tool", "search", state["q"])
        return ("final", "answer: " + (state["obs"][-1] if state["obs"] else "unknown"))

def run_agent(q, llm, max_steps=5, token_budget=1000, tok_per_step=300, record=None, replay=None):
    state, tokens, calls, log = {"q": q, "obs": [], "steps": 0}, 0, [], []
    while state["steps"] < max_steps:
        if tokens + tok_per_step > token_budget: return {"final": "stopped: budget", "tokens": tokens, "calls": calls, "log": log}
        tokens += tok_per_step
        act = replay.pop(0) if replay is not None else llm.next(state)   # replay: recorded LLM outputs, no model
        if record is not None: record.append(act)
        log.append(act); state["steps"] += 1
        if act[0] == "final": return {"final": act[1], "tokens": tokens, "calls": calls, "log": log}
        _, name, arg = act
        if name in FORBIDDEN: return {"final": "blocked tool " + name, "tokens": tokens, "calls": calls, "log": log}   # policy guard
        calls.append(name); state["obs"].append(FIXTURES.get((name, arg), "no data"))
    return {"final": "stopped: max_steps", "tokens": tokens, "calls": calls, "log": log}

# 1. golden trajectory with tolerance on steps (tool sequence must match, step count may be within +1)
r = run_agent("pune weather", MockLLM(1))
assert r["final"] == "answer: 31C sunny" and r["calls"] == ["search"] and len(r["log"]) in (2, 3)
# 2. budget invariant over many seeds and budgets: tokens never exceed the budget
for seed in range(50):
    for budget in (0, 300, 600, 1000):
        out = run_agent("pune weather", MockLLM(seed, wobble=0.5), token_budget=budget)
        assert out["tokens"] <= budget, (seed, budget, out["tokens"])
# 3. forbidden-tool invariant: a policy-violating model must never get the tool executed
out = run_agent("pune weather", MockLLM(1, bad_tool=True))
assert "delete_account" not in out["calls"] and out["final"].startswith("blocked")
# 4. replay determinism: record one run, replay its LLM outputs, get the identical result
rec = []; first = run_agent("mumbai weather", MockLLM(7, wobble=0.3), record=rec)
again = run_agent("mumbai weather", None, replay=list(rec))
assert json.dumps(first, sort_keys=True) == json.dumps(again, sort_keys=True)
# 5. flaky behaviour: repeat N runs and assert a pass-rate threshold instead of a single pass/fail
def passes(seed): return run_agent("pune weather", MockLLM(seed, wobble=0.1))["final"] == "answer: 31C sunny"
rate = sum(passes(s) for s in range(100)) / 100
print(f"golden ok, budget invariant ok (200 runs), forbidden-tool guard ok, replay identical")
print(f"pass rate over 100 seeded runs with 10% wobble = {rate:.2f} (threshold >= 0.80)")
assert rate >= 0.80
print("tests passed")
