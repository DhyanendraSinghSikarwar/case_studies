# Retry cost. Illustrative price: 3 per million input tokens; timed-out calls are billed (stated assumption).
calls, rate, prompt, retries = 100_000, 0.08, 3000, 3
price = 3.0
timeouts = round(calls * rate)
tok_per_round = timeouts * prompt
cost_round = tok_per_round / 1e6 * price
base_cost = calls * prompt / 1e6 * price
print("timeouts", timeouts, "tokens per retry round", tok_per_round, "cost per retry round", cost_round)
print("baseline first-attempt daily input cost", base_cost)
low = cost_round * 1
high = cost_round * retries
print("extra if every timeout succeeds on retry 1:", low, f"({low/base_cost:.0%} of base)")
print("extra upper bound if all 3 retries used:", high, f"({high/base_cost:.0%} of base)")
assert timeouts == 8000 and tok_per_round == 24_000_000
assert cost_round == 72 and base_cost == 900 and low == 72 and high == 216
assert round(low/base_cost, 3) == 0.08 and round(high/base_cost, 3) == 0.24
# Expected under a more realistic mix (illustrative): each retry times out again with prob q
q = 0.5
exp_attempts = sum(q**i for i in range(retries))      # retries sent per original timeout, stops on success
exp_extra = timeouts * exp_attempts * prompt / 1e6 * price
print("expected extra with q=0.5 re-timeout chance:", round(exp_extra, 1), "attempts/timeout", exp_attempts)
assert exp_attempts == 1.75 and round(exp_extra, 1) == 126.0
# Monthly (30 days) for the upper bound
print("30-day upper bound", high * 30)
assert high * 30 == 6480
