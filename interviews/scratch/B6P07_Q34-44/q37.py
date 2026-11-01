# Illustrative numbers from the prompt (price is illustrative, not a vendor price)
SYS, NEW, TURNS, PRICE = 1000, 300, 20, 3.0   # tokens, tokens/turn, turns, price per million input tokens

inp = [SYS + NEW * t for t in range(1, TURNS + 1)]   # system prompt + the new tokens of each of the t turns so far
total = sum(inp)
print("input at turn 1, 10, 20:", inp[0], inp[9], inp[19])
print("total input tokens:", total, "| cost:", round(total * PRICE / 1e6, 4))
assert inp[0] == 1300 and inp[9] == 4000 and inp[19] == 7000
assert total == 20 * SYS + NEW * sum(range(1, 21)) == 20_000 + 300 * 210 == 83_000
assert round(total * PRICE / 1e6, 3) == 0.249

base = TURNS * (SYS + NEW)   # no history resent: system prompt plus the turn's own 300 tokens
print(f"no-history baseline {base}; ratio {total/base:.2f}")
assert base == 26_000 and round(total / base, 2) == 3.19

# Growth is quadratic in turns
total40 = sum(SYS + NEW * t for t in range(1, 41))
print("40 turns:", total40, "tokens, x%.2f of 20 turns" % (total40 / total))
assert total40 == 40 * 1000 + 300 * 820 == 286_000 and round(total40 / total, 2) == 3.45

# Policy A: keep the system prompt plus only the last 5 turns (including the current one)
K = 5
win = sum(SYS + NEW * min(t, K) for t in range(1, TURNS + 1))
print("sliding window (last 5 turns):", win, "tokens,", f"{win/total:.0%} of full history")
assert win == 20_000 + 300 * (sum(range(1, 6)) + 15 * 5) == 47_000 and round(win / total, 2) == 0.57

# Policy B: prefix caching, previously sent tokens billed at 10% of the input rate (illustrative)
CACHE = 0.10
eff = inp[0] + sum(CACHE * inp[t - 2] + NEW for t in range(2, TURNS + 1))   # turn t re-reads turn t-1's input as prefix
eff_cost = eff * PRICE / 1e6
print(f"with prefix cache: effective tokens {eff:.0f}, cost {eff_cost:.4f} ({eff/total:.0%} of uncached)")
assert round(eff) == 14_600 and round(eff / total, 2) == 0.18

# Other numbers quoted in the text
print("20 x last turn:", 20 * inp[19], "| turn 20 with window:", SYS + NEW * K)
assert 20 * inp[19] == 140_000 and SYS + NEW * K == 2_500 and inp[19] - SYS == 6_000
