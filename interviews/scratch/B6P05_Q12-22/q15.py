# Illustrative numbers.
alerts, frauds, cap, rev_cost, loss = 5000, 500, 2000, 3.0, 90.0
top_frauds = 360
assert frauds / alerts == 0.10 and top_frauds / cap == 0.18
review_cost = cap * rev_cost
top_gross = top_frauds * loss                 # assumes review catches the fraud and prevents the full loss
rand_frauds = cap * frauds / alerts
rand_gross = rand_frauds * loss
print(f"review cost {review_cost:,.0f}")
print(f"top 2000: frauds {top_frauds} gross {top_gross:,.0f} net {top_gross-review_cost:,.0f}")
print(f"random 2000: frauds {rand_frauds:.0f} gross {rand_gross:,.0f} net {rand_gross-review_cost:,.0f}")
assert (review_cost, top_gross, rand_gross) == (6000, 32400, 18000)
assert (top_gross - review_cost, rand_gross - review_cost) == (26400, 12000)
print("value of ranking (top minus random):", top_gross - rand_gross)
assert top_gross - rand_gross == 14400
# Break-even precision for one review
be = rev_cost / loss
print(f"break-even precision for a review: {be:.2%}")
assert round(be, 4) == 0.0333
# The 3,000 nobody reviews
rest_n, rest_f = alerts - cap, frauds - top_frauds
print(f"unreviewed: {rest_n} alerts, {rest_f} frauds, precision {rest_f/rest_n:.2%}, exposure {rest_f*loss:,.0f}")
assert (rest_n, rest_f) == (3000, 140) and round(rest_f / rest_n, 4) == 0.0467 and rest_f * loss == 12600
print(f"average precision of the unreviewed pool is above break-even: {rest_f/rest_n > be}")
assert rest_f / rest_n > be
# If extra review capacity could be added at the same 3 per alert and the average precision held:
extra_net = rest_f * loss - rest_n * rev_cost
print(f"reviewing all 3000 at the pool average would net {extra_net:,.0f}")
assert extra_net == 3600
# But the pool is ranked: the marginal precision at rank 2001 is below the pool average. Illustrative bands:
bands = [(1000, 0.065), (1000, 0.045), (1000, 0.030)]   # (alerts, fraud rate) of ranks 2001-5000
tot = sum(n * p for n, p in bands)
print("bands add to", round(tot), "frauds")
assert round(tot) == 140
for n, p in bands:
    print(f"band of {n}: precision {p:.2%}  net of review {n*p*loss - n*rev_cost:+,.0f}")
assert (1000 * 0.030 * loss - 1000 * rev_cost) < 0 < (1000 * 0.045 * loss - 1000 * rev_cost)
