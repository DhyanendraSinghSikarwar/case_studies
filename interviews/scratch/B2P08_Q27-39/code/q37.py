# Cost/latency simulator with ASSUMED numbers (not measurements): sequential vs parallel sub-agents, model routing, budgets, caching.
PRICE = {"big": 15.0, "small": 3.0}          # ASSUMED $ per 1M tokens, same for in/out for simplicity
SEC_PER_CALL = {"big": 8.0, "small": 3.0}    # ASSUMED seconds per sub-agent task
TOK_PER_TASK = 20_000                        # ASSUMED tokens per sub-agent task
LEAD_TOKENS, LEAD_SECONDS = 10_000, 8.0      # ASSUMED lead plan + combine

def run(n_tasks, mode="sequential", worker="big", lead="big", cached_prefix=0.0, budget_tokens=None):
    done, tokens, cost = 0, 0, 0.0
    tokens += LEAD_TOKENS; cost += LEAD_TOKENS * PRICE[lead] / 1e6
    per_task = TOK_PER_TASK * (1 - cached_prefix * 0.5)      # ASSUMED: cached part costs half of a normal token
    for _ in range(n_tasks):
        if budget_tokens is not None and tokens + per_task > budget_tokens: break   # hard budget: stop launching
        tokens += per_task; cost += per_task * PRICE[worker] / 1e6; done += 1
    t = SEC_PER_CALL[worker]
    secs = LEAD_SECONDS + (done * t if mode == "sequential" else (t if done else 0))
    return dict(done=done, tokens=int(tokens), cost=round(cost, 3), secs=round(secs, 1))

cases = {
 "5 tasks sequential, all big":      run(5),
 "5 tasks parallel, all big":        run(5, "parallel"),
 "5 parallel, small workers":        run(5, "parallel", worker="small"),
 "5 parallel, small + 60% cached":   run(5, "parallel", worker="small", cached_prefix=0.6),
 "5 parallel big, budget 70k":       run(5, "parallel", budget_tokens=70_000),
}
for k, v in cases.items(): print(f"{k:34}", v)
a, b, c = cases["5 tasks sequential, all big"], cases["5 tasks parallel, all big"], cases["5 parallel, small workers"]
assert b["secs"] < a["secs"] and b["cost"] == a["cost"]         # parallelism cuts latency, not cost
assert c["cost"] < b["cost"] and cases["5 parallel big, budget 70k"]["done"] == 3
print("tests passed")
