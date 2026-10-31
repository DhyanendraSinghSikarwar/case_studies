ttft, tps, tokens, budget = 0.8, 40.0, 300, 5.0
gen = tokens / tps
last = ttft + gen
print(f"generation time {gen:.2f}s; time to last token {last:.2f}s; over budget by {last-budget:.2f}s")
assert gen == 7.5 and round(last, 1) == 8.3 and round(last-budget, 1) == 3.3
print(f"first visible text: streaming {ttft:.1f}s (plus network/render), no streaming {last:.1f}s")
# What fits in 5 s at 40 tok/s?
max_tokens = (budget - ttft) * tps
print(f"max answer length inside budget at 40 tok/s: {max_tokens:.0f} tokens"); assert round(max_tokens) == 168
# Or what speed is needed for 300 tokens?
need = tokens / (budget - ttft); print(f"needed speed for 300 tokens: {need:.1f} tok/s"); assert round(need, 1) == 71.4
# Options (illustrative)
for name, t, s, n in [("shorter answer 300->150", ttft, tps, 150),
                      ("faster decode 40->80 tok/s", ttft, 80, 300),
                      ("both, TTFT 0.8->0.5", 0.5, 80, 150),
                      ("only TTFT 0.8->0.3", 0.3, 40, 300)]:
    print(f"{name:28} last token {t + n/s:.2f}s")
assert 0.8 + 150/40 == 4.55 and 0.8 + 300/80 == 4.55 and 0.5 + 150/80 == 2.375 and 0.3 + 300/40 == 7.8
# Reading speed rule of thumb (editor knowledge, not measured here): ~4 words/s, ~1.3 tokens/word -> ~5 tokens/s
read_tps = 4*1.3
print(f"reader keeps pace at ~{read_tps:.1f} tok/s; stream is {tps/read_tps:.1f}x faster; reading 300 tokens takes ~{tokens/read_tps:.0f}s")
assert round(tps/read_tps, 1) == 7.7
