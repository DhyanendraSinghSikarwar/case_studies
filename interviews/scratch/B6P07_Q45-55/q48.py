tasks, tail_n, tail_tok, med = 100_000, 1_000, 160_000, 20_000
body_n = tasks - tail_n
total = body_n*med + tail_n*tail_tok
tail = tail_n*tail_tok
print(f"total tokens = {total:,}, tail tokens = {tail:,}")
assert total == 2_140_000_000 and tail == 160_000_000
share = tail/total
print(f"tail share of tokens = {share:.4f} while the tail is {tail_n/tasks:.1%} of tasks")
assert round(share, 4) == 0.0748
cap = 80_000
saved = tail_n*(tail_tok - cap)
print(f"tokens saved by cap = {saved:,} = {saved/total:.4f} of all tokens")
assert saved == 80_000_000 and round(saved/total, 4) == 0.0374
# retries of capped tasks as fresh runs reduce the saving
for r in (0.0, 0.5, 1.0):
    net = saved - r*tail_n*cap
    print(f"if {r:.0%} of capped tasks are rerun from scratch up to the cap: net saving {net:,.0f} = {net/total:.4f}")
assert saved - 1.0*tail_n*cap == 0
# illustrative money at a blended 5 per million tokens
price = 5
print(f"illustrative money: total {total*price/1e6:,.0f}, saving {saved*price/1e6:,.0f}")
assert total*price/1e6 == 10_700 and saved*price/1e6 == 400
# real distributions: if the other 99,000 average 25,000 instead of exactly 20,000
total2 = body_n*25_000 + tail
print(f"if the body averages 25,000: tail share {tail/total2:.4f}, cap saving {saved/total2:.4f}")
assert round(tail/total2, 4) == 0.0607 and round(saved/total2, 4) == 0.0304
low = tail_n*(tail_tok - 40_000)
print(f"cap at 40,000 saves {low:,} = {low/total:.4f}")
assert low == 120_000_000 and round(low/total, 3) == 0.056
