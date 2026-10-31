# Q36: cost-per-1000-requests model in abstract units (invented). 10x sensitivity.
base_rps = 100  # requests per second at today's peak
unit = dict(feature_read=0.002, gpu_ms=0.0004, embed_refresh=0.5, log_byte=0.00000002)  # abstract units
def cost_per_1k(mult, cache_hit=0.0, cand=500, rank_ms_per_cand=0.02, refresh_per_day=4, logged_bytes=2000, daily_req=None):
    daily = (daily_req or 86400 * base_rps * 0.3) * mult        # 30% duty cycle, invented
    reads = daily * (1 - cache_hit) * 20 * unit["feature_read"] * mult**0.15   # invented hot-key / extra-shard overhead
    gpu   = daily * cand * rank_ms_per_cand * unit["gpu_ms"]
    emb   = refresh_per_day * unit["embed_refresh"] * 1000 * mult**0.5   # item catalogue grows slower than traffic (invented)
    logs  = daily * logged_bytes * unit["log_byte"]
    total = reads + gpu + emb + logs
    return 1000 * total / daily, dict(reads=reads, gpu=gpu, emb=emb, logs=logs, daily=daily)
print(f"{'case':34s}{'x':>4s}{'cost/1k':>9s}   biggest")
cases = [("today", 1, {}), ("10x naive", 10, {}),
         ("10x + cache 60%", 10, dict(cache_hit=0.6)),
         ("10x + cache + cand 500->200", 10, dict(cache_hit=0.6, cand=200)),
         ("10x + cache + cand + log sample 20%", 10, dict(cache_hit=0.6, cand=200, logged_bytes=400)),
         ("... + refresh 4->2/day (negotiated)", 10, dict(cache_hit=0.6, cand=200, logged_bytes=400, refresh_per_day=2))]
res = {}
for name, m, kw in cases:
    c, parts = cost_per_1k(m, **kw); res[name] = c
    big = max(("reads", "gpu", "emb", "logs"), key=parts.get)
    print(f"{name:34s}{m:>4d}{c:9.4f}   {big}")
assert res["10x + cache + cand + log sample 20%"] <= res["today"]
print("flat vs today?", round(res["10x + cache + cand + log sample 20%"] / res["today"], 2), "x today")
print("sensitivity of 10x naive to unit costs (each +50%):")
b = res["10x naive"]
for k in unit:
    old = unit[k]; unit[k] = old * 1.5; c, _ = cost_per_1k(10); unit[k] = old
    print(f"  {k:14s} -> {c/b:5.3f} x base")
