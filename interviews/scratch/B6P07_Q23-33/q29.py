# TTFT budget: sequential versus parallel moderation. Illustrative stage times in ms.
mod, ret, rer, ttft_model, budget = 100, 250, 150, 400, 700
seq = mod + ret + rer + ttft_model
par = max(mod, ret) + rer + ttft_model
print("sequential", seq, "over budget by", seq - budget)
print("moderation parallel with retrieval", par, "over budget by", par - budget)
assert seq == 900 and par == 800 and par - budget == 100 and seq - par == mod
# Critical path: moderation also fully off the path (runs alongside retrieval+rerank), nothing changes
par_all = max(mod, ret + rer) + ttft_model
print("moderation alongside retrieval+rerank", par_all)
assert par_all == 800
# Options to reach 700 (illustrative cuts)
opts = {
 "rerank over fewer candidates (150 -> 60)": par - (150 - 60),
 "rerank 150 -> 60 and retrieval 250 -> 200": par - (150 - 60) - 50,
 "smaller prompt cuts TTFT 400 -> 320": par - 80,
 "skip rerank for easy queries (150 -> 0 on 40% of queries), mean": par - 0.4 * 150,
}
for k, v in opts.items():
    print(f"{k}: {v:.0f}")
assert opts["rerank over fewer candidates (150 -> 60)"] == 710
assert opts["rerank 150 -> 60 and retrieval 250 -> 200"] == 660
assert opts["smaller prompt cuts TTFT 400 -> 320"] == 720
assert opts["skip rerank for easy queries (150 -> 0 on 40% of queries), mean"] == 740
# Cut needed
print("cut needed after parallelising:", par - budget)
