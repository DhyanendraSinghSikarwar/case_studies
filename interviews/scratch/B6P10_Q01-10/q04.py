# Q4 support RAG cost: illustrative prices from the prompt
chats, in_tok, out_tok = 60_000, 4_000, 300
p_in, p_out, ceiling = 0.30, 1.20, 2.00     # rupees per 1,000 tokens (illustrative)
c_in = in_tok / 1000 * p_in
c_out = out_tok / 1000 * p_out
per_chat = c_in + c_out
daily = chats * per_chat
headroom = ceiling - per_chat
print(f"input {c_in:.2f} + output {c_out:.2f} = {per_chat:.2f} per chat; daily {daily:,.0f}; 30 days {daily*30:,.0f}")
print(f"headroom {headroom:.2f} per chat = {headroom/ceiling:.0%} of ceiling; ceiling-level daily {ceiling*chats:,.0f}")
extra_in_tokens = headroom / p_in * 1000
print(f"headroom equals about {extra_in_tokens:,.0f} extra input tokens per chat")
# illustrative tiering: 60% of chats go to a model priced at one fifth
tier = 0.4 * per_chat + 0.6 * per_chat / 5
print(f"illustrative tiered cost per chat {tier:.3f}, daily {tier*chats:,.0f}")
# latency: why 'first answer' must mean first token / first chunk
gen_rate = 60  # tokens per second, assumption
full_gen_s = out_tok / gen_rate
print(f"full 300-token answer at {gen_rate} tok/s takes {full_gen_s:.1f} s, over the 4 s budget")
split = {"input guard": 100, "retrieve": 150, "rerank": 150, "prompt build": 50, "first token": 800, "streaming to user": 100}
print(split, sum(split.values()))
avg_cps = chats / 86_400
print(f"average {avg_cps:.2f} chats/s")
assert round(c_in, 2) == 1.20 and round(c_out, 2) == 0.36 and round(per_chat, 2) == 1.56
assert round(daily) == 93_600 and round(headroom, 2) == 0.44
assert round(headroom / ceiling, 2) == 0.22 and round(extra_in_tokens) == 1467
assert round(tier, 3) == 0.811 and round(full_gen_s, 1) == 5.0
assert sum(split.values()) == 1350 and sum(split.values()) < 4000
assert round(avg_cps, 2) == 0.69
