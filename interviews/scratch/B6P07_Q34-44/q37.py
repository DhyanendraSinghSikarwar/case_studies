# Illustrative numbers from the prompt (price is illustrative, not a vendor price)
SYS, NEW, TURNS, PRICE = 1000, 300, 20, 3.0   # tokens, tokens/turn, turns, price per million input tokens

inp = [SYS + NEW * (t - 1) for t in range(1, TURNS + 1)]   # prompt's formula: system + (t-1) earlier turns
total = sum(inp)
print("input at turn 1, 10, 20:", inp[0], inp[9], inp[19])
print("total input tokens:", total, "| cost:", round(total * PRICE / 1e6, 4))
assert inp[0] == 1000 and inp[9] == 3700 and inp[19] == 6700
assert total == 20 * SYS + NEW * sum(range(20)) == 20_000 + 300 * 190 == 77_000
assert round(total * PRICE / 1e6, 3) == 0.231

# The prompt compares with 20,000 (system prompt only). That baseline leaves out the 300 new tokens
# each turn actually has to send. Like-for-like "no history resent": system + the turn's own 300 tokens.
base_prompt = TURNS * SYS
base_fair = TURNS * (SYS + NEW)
print(f"vs prompt baseline 20,000: x{total/base_prompt:.2f}; vs like-for-like {base_fair}: x{total/base_fair:.2f}")
assert base_prompt == 20_000 and base_fair == 26_000
assert round(total / base_prompt, 2) == 3.85 and round(total / base_fair, 2) == 2.96

# Growth is quadratic in turns: doubling the conversation length
total40 = sum(SYS + NEW * (t - 1) for t in range(1, 41))
print("40 turns:", total40, "tokens, x%.2f of 20 turns" % (total40 / total))
assert total40 == 40 * 1000 + 300 * 780 and round(total40 / total, 2) == 3.56

# Policy A: keep the system prompt plus only the last 5 turns
K = 5
win = sum(SYS + NEW * min(t - 1, K) for t in range(1, TURNS + 1))
print("sliding window (last 5 turns):", win, "tokens,", f"{win/total:.0%} of full history")
assert win == 20_000 + 300 * (sum(range(1, 6)) + 14 * 5) == 45_500 and round(win / total, 2) == 0.59

# Policy B: prefix caching, previously sent tokens billed at 10% of the input rate (illustrative)
CACHE = 0.10
eff = inp[0] + sum(CACHE * inp[t - 2] + NEW for t in range(2, TURNS + 1))   # turn t re-reads input of turn t-1 as prefix
eff_cost = eff * PRICE / 1e6
print(f"with prefix cache: effective tokens {eff:.0f}, cost {eff_cost:.4f} ({eff/total:.0%} of uncached)")
assert round(eff) == 13_730 and round(eff / total, 2) == 0.18

# Other numbers quoted in the text
alt_total = sum(SYS + NEW * t for t in range(1, TURNS + 1))   # if the current message is also counted
print("if the current message is also counted:", alt_total, "| 20 x last turn:", 20 * inp[19], "| turn 20 with window:", SYS + NEW * K)
assert alt_total == 83_000 and 20 * inp[19] == 134_000 and SYS + NEW * K == 2_500 and inp[19] - SYS == 5_700
