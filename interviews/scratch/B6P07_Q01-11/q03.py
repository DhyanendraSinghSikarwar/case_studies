# ILLUSTRATIVE round prices, not any vendor's prices: 3 per million input tokens, 15 per million output tokens
PIN, POUT = 3.0, 15.0
def call_cost(tin, tout, pin=PIN, pout=POUT): return (tin*pin + tout*pout) / 1e6
calls_day, days = 50_000, 30
base = call_cost(2000, 400)
month = base * calls_day * days
print(f"per call {base:.4f}; per day {base*calls_day:,.0f}; per month {month:,.0f}; budget 6,000 -> {month/6000:.1f}x")
assert round(base, 6) == 0.012 and round(month) == 18000 and month == 3*6000
print(f"input share {2000*PIN/1e6/base:.0%}, output share {400*POUT/1e6/base:.0%}")
assert 2000*PIN/1e6/base == 0.5
# Lever 1: shorter answers, 400 -> 250 output tokens
l1 = call_cost(2000, 250); s1 = (base - l1) * calls_day * days
print(f"L1 cap output at 250: saves {s1:,.0f}/month ({s1/month:.1%})"); assert round(s1) == 3375
# Lever 2: cache a static 1,500-token prefix; cached tokens at 10% of input price (illustrative), 80% hit rate
hit, cache_price = 0.8, 0.10*PIN
eff_in = 1500*(hit*cache_price + (1-hit)*PIN)/1e6 + 500*PIN/1e6
l2 = eff_in + 400*POUT/1e6; s2 = (base - l2) * calls_day * days
print(f"L2 prefix cache: saves {s2:,.0f}/month ({s2/month:.1%})"); assert round(s2) == 4860
# Lever 3: route 50% of calls to a model at one fifth of the prices
share, ratio = 0.5, 0.2
s3 = base * share * (1 - ratio) * calls_day * days
print(f"L3 route 50% to a 1/5-price model: saves {s3:,.0f}/month ({s3/month:.1%})"); assert round(s3) == 7200
# Combined (apply in order, savings overlap): L1 and L2 on all calls, then L3 on half
combo_call = (eff_in + 250*POUT/1e6)
combo = combo_call*(1 - share) * calls_day*days + combo_call*ratio*share * calls_day*days
print(f"all three together: {combo:,.0f}/month; budget 6,000"); assert round(combo) == 5859
print("single levers do not add up; sum would be", round(s1+s2+s3), "but combined saving is", round(month-combo))
assert combo < 6000 < month and (s1+s2+s3) > (month - combo)
