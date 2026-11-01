# Q23 alert triage buckets (illustrative, retrospective counts)
b = {"top": (3_000, 270), "middle": (3_000, 24), "bottom": (4_000, 6)}
total_alerts = sum(n for n, _ in b.values())
total_conf = sum(c for _, c in b.values())
assert total_alerts == 10_000 and total_conf == 300
rate = {k: c / n for k, (n, c) in b.items()}
assert round(rate["top"], 4) == 0.09 and round(rate["middle"], 4) == 0.008 and round(rate["bottom"], 5) == 0.0015
print({k: f"{v:.2%}" for k, v in rate.items()}, f"overall {total_conf/total_alerts:.1%}")

top2 = b["top"][1] + b["middle"][1]
share = top2 / total_conf
assert top2 == 294 and share == 0.98
print(f"top two buckets: 6,000 alerts, {top2} of {total_conf} confirmed = {share:.0%}")
print(f"missed if bottom never reviewed: {b['bottom'][1]} cases ({b['bottom'][1]/total_conf:.0%})")

# Lift versus random review of 6,000 alerts
random_found = 6_000 * (total_conf / total_alerts)
assert random_found == 180
print(f"random order would find ~{random_found:.0f}; model finds {top2}")

# Sampling the bottom bucket: how many to read to expect to see >=1 case with 95% probability at 0.15%?
import math
n95 = math.log(0.05) / math.log(1 - rate["bottom"])
assert 1_990 < n95 < 2_010
print(f"alerts to sample for 95% chance of seeing one case at 0.15%: {n95:,.0f}")
# A 5% monthly sample of the bottom bucket
sample = 0.05 * 4_000
exp_cases = sample * rate["bottom"]
assert sample == 200 and abs(exp_cases - 0.3) < 1e-9
print(f"5% sample = {sample:.0f} alerts, expected cases {exp_cases:.1f}: far too few to track the rate monthly")
