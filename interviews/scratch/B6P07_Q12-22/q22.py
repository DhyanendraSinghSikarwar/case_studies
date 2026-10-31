calls = 1_000_000
prefix, var, price, disc = 4_000, 500, 3.0, 0.10         # illustrative price per million input tokens
per_m = lambda tok: tok * calls * price / 1e6
no_cache = per_m(prefix + var)
def with_hit(h, write_mult=1.0):
    hit = per_m(prefix) * h * disc
    miss = per_m(prefix) * (1 - h) * write_mult
    return hit + miss + per_m(var)
c60 = with_hit(0.6)
print(f"no cache {no_cache:,.0f}; 60% hit {c60:,.0f}; saving {no_cache-c60:,.0f} = {(no_cache-c60)/no_cache:.1%}")
assert no_cache == 13_500 and round(c60) == 7_020 and round((no_cache - c60) / no_cache, 3) == 0.48
for h in (0.0, 0.3, 0.6, 0.9, 1.0):
    print(f"hit rate {h:.0%}: {with_hit(h):,.0f}")
assert round(with_hit(1.0)) == 2_700 and round((no_cache - with_hit(1.0)) / no_cache, 2) == 0.80
c60w = with_hit(0.6, 1.25)
print(f"if misses carried an invented 1.25x write premium: 60% hit {c60w:,.0f}, saving {(no_cache-c60w)/no_cache:.1%}")
assert round(c60w) == 8_220 and round((no_cache - c60w) / no_cache, 3) == 0.391
# Prompt layout: only an identical leading run of tokens can hit.
def shared_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n
sys_p = ["SYS"] * 10 + ["RULES"] * 5
bad_a = ["t=10:01"] + sys_p + ["Q:refund"]; bad_b = ["t=10:02"] + sys_p + ["Q:order"]
good_a = sys_p + ["t=10:01", "Q:refund"]; good_b = sys_p + ["t=10:02", "Q:order"]
print("timestamp first -> shared prefix", shared_prefix(bad_a, bad_b), "of", len(bad_a), "| timestamp last ->", shared_prefix(good_a, good_b), "of", len(good_a))
assert shared_prefix(bad_a, bad_b) == 0 and shared_prefix(good_a, good_b) == 15
