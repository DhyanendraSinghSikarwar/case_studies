# Q28 LLM analytics assistant cost (illustrative prices)
qpd, calls, tok, price_k, budget, days = 5_000, 2.4, 6_000, 0.25, 60_000, 30
tokens_day = qpd * calls * tok
cost_day = tokens_day / 1000 * price_k
cost_month = cost_day * days
factor = cost_month / budget
assert tokens_day == 72_000_000 and cost_day == 18_000 and cost_month == 540_000 and factor == 9
print(f"tokens/day={tokens_day:,.0f}, cost/day={cost_day:,.0f}, cost/month={cost_month:,.0f}, factor over budget={factor:.0f}x")
per_q = calls * tok / 1000 * price_k
allowed = budget / days / qpd
assert abs(per_q - 3.6) < 1e-9 and abs(allowed - 0.4) < 1e-9
print(f"cost per question={per_q:.2f} rupees, allowed={allowed:.2f}")

# Lever A: route 80% of calls to a small model priced at 0.1x (assumed)
price_factor = 0.2 + 0.8 * 0.1
a = 1 / price_factor
# Lever B: cut tokens per call 6,000 -> 2,000 (schema pruning, short context)
b = 6_000 / 2_000
assert abs(a - 3.5714) < 1e-3 and b == 3
both = a * b
new_month = cost_month / both
assert abs(both - 10.714) < 1e-2 and new_month < budget and abs(new_month - 50_400) < 1
print(f"routing alone {a:.2f}x, token cut alone {b:.1f}x (neither reaches 9x), both {both:.2f}x -> {new_month:,.0f} per month")
# Lever C: answer cache with 30% hit rate adds headroom
c = 1 / 0.7
assert abs(both * c - 15.31) < 0.01
print(f"adding a 30% cache hit rate: {both*c:.2f}x -> {cost_month/(both*c):,.0f} per month")

# Alternative reading: 6,000 tokens per question in total
alt = qpd * 6_000 / 1000 * price_k * days
assert alt == 225_000 and abs(alt / budget - 3.75) < 1e-9
print(f"if 6,000 tokens were per question: {alt:,.0f} per month, {alt/budget:.2f}x over")
