# Illustrative prices and volumes (not vendor prices). Prompt-growth cost and a caching sensitivity.
calls, price_in = 2_000_000, 3.0           # calls per month, price per million input tokens
old, new = 800, 3500
extra_tokens_per_call = new - old
extra_tokens = extra_tokens_per_call * calls
extra_cost = extra_tokens / 1e6 * price_in
old_cost = old * calls / 1e6 * price_in
new_cost = new * calls / 1e6 * price_in
print("extra tokens per call", extra_tokens_per_call, "extra tokens per month", extra_tokens)
print("old prompt cost", old_cost, "new prompt cost", new_cost, "extra", extra_cost)
assert extra_tokens_per_call == 2700 and extra_tokens == 5_400_000_000
assert old_cost == 4800 and new_cost == 21000 and extra_cost == 16200
assert round(new / old, 3) == 4.375
# Sensitivity: trim back to 1,500 tokens
trim = 1500
saved = (new - trim) * calls / 1e6 * price_in
print("trim to", trim, "saves", saved, "per month; remaining extra", (trim - old) * calls / 1e6 * price_in)
assert saved == 12000 and (trim - old) * calls / 1e6 * price_in == 4200
# Sensitivity: if the stable prefix is cached at an illustrative 10% of the input rate with an 80% hit rate
hit, disc = 0.8, 0.10
eff = (1 - hit) + hit * disc               # effective fraction of full price paid on the prefix
print("effective price fraction", round(eff, 2), "extra cost with caching", round(extra_cost * eff, 1))
assert round(eff, 2) == 0.28 and round(extra_cost * eff, 1) == 4536.0
