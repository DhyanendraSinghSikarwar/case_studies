import math
import numpy as np

# Prompt arithmetic: typical (mean) path latency, sequential
llm_steps, llm_s, tool_calls, tool_s, budget = 4, 1.5, 3, 0.4, 12.0
typical = llm_steps * llm_s + tool_calls * tool_s
slack = budget - typical
assert abs(typical - 7.2) < 1e-9 and abs(slack - 4.8) < 1e-9
print("typical latency (s):", typical, "| slack to 12 s budget (s):", round(slack, 1))

# The budget is for the 95th percentile, not the typical run. Illustrative simulation:
# each step is lognormal with the stated mean and a coefficient of variation of 0.4 (my assumption).
rng = np.random.default_rng(13)
def lognormal_with_mean(mean, cv, size):
    s2 = math.log(1 + cv ** 2)
    return rng.lognormal(math.log(mean) - s2 / 2, math.sqrt(s2), size)
N = 200_000
total = sum(lognormal_with_mean(llm_s, 0.4, N) for _ in range(llm_steps)) \
      + sum(lognormal_with_mean(tool_s, 0.4, N) for _ in range(tool_calls))
p95 = float(np.percentile(total, 95))
print("simulated mean:", round(float(total.mean()), 2), "| simulated p95:", round(p95, 2))
assert abs(total.mean() - 7.2) < 0.05 and p95 > typical
print("p95 within 12 s budget in this simulation:", p95 < budget)
# With one retry on each LLM step with 10% probability, the tail grows (assumed retry rate)
retry = rng.random((llm_steps, N)) < 0.10
extra = sum(retry[i] * lognormal_with_mean(llm_s, 0.4, N) for i in range(llm_steps))
p95_retry = float(np.percentile(total + extra, 95))
print("p95 with 10% retry per LLM step:", round(p95_retry, 2))
assert p95_retry > p95

# Load: 20,000 requests a day is small; Little's law for average concurrency (even spread, a simplification)
rate = 20_000 / 86_400
conc = rate * typical
print("average requests/s:", round(rate, 3), "| average concurrent runs:", round(conc, 2))
assert round(rate, 3) == 0.231 and round(conc, 2) == 1.67

# Evaluation budget: if a staged test shows 0 wrong refunds in n independent runs, the 95% upper bound on the error rate is about 3/n
n_zero = math.ceil(math.log(0.05) / math.log(1 - 0.01))
print("clean runs needed to bound wrong-refund rate below 1% at 95%:", n_zero)
assert n_zero == 299 and (1 - 0.01) ** n_zero <= 0.05 < (1 - 0.01) ** (n_zero - 1)
