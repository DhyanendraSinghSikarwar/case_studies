from math import sqrt
# Illustrative funnel for one week of a GenAI shopping assistant
eligible = 100_000        # sessions where the entry point was shown (exposure)
asked    = 20_000         # opened and asked a question (engagement)
answered = 18_800         # got a real answer (no error, no refusal)
clicked  = 9_400          # clicked a product or link from the answer
good_clk = 8_000          # clicks that did not bounce back within 10 s and were not followed by a rephrase
noclick  = answered - clicked
print(f"engagement {asked / eligible:.1%}, answer rate {answered / asked:.1%}, click rate {clicked / answered:.1%}")
assert noclick == 9_400
# human-labelled random sample of no-click sessions
sample = 400
good, bad, unclear = 240, 100, 60
assert good + bad + unclear == sample
p = good / sample
half = 1.96 * sqrt(p * (1 - p) / sample)
print(f"labelled good abandonment {p:.0%} (95% CI {p - half:.1%} to {p + half:.1%})")
assert round(p, 2) == 0.60 and round(half, 3) == 0.048
succ_click_only = good_clk / answered
succ_est = (good_clk + p * noclick) / answered
print(f"success, click-based    {succ_click_only:.1%}")
print(f"success, label-adjusted {succ_est:.1%}")
assert round(succ_click_only, 3) == 0.426 and round(succ_est, 3) == 0.726
# cost (illustrative Rs per answered session)
cost = 0.40
total_cost = cost * answered
n_succ = good_clk + p * noclick
print(f"cost per answered session Rs {cost:.2f}; per successful session Rs {total_cost / n_succ:.2f}")
assert round(total_cost / n_succ, 2) == 0.55
# incremental view: holdout (no assistant), orders per 100 sessions
treat_orders_per_100, hold_orders_per_100 = 3.30, 3.10
print(f"incremental orders per 100 exposed sessions {treat_orders_per_100 - hold_orders_per_100:.2f}")
assert round(treat_orders_per_100 - hold_orders_per_100, 2) == 0.20
