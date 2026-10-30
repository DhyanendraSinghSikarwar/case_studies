# Q30 marketplace: listings +25%, buyer conversion 5.0% -> 4.2% (illustrative numbers)
sessions = 1_000_000
share_old_heavy, share_new_heavy = 0.75, 0.25   # sessions whose top results are mostly old / mostly new listings

worlds = {
    "A: quality dilution":  {"old-heavy": 0.050, "new-heavy": 0.018},
    "B: ranking/search bug": {"old-heavy": 0.042, "new-heavy": 0.042},
}
for name, w in worlds.items():
    blended = share_old_heavy * w["old-heavy"] + share_new_heavy * w["new-heavy"]
    print(f"{name:24} old-heavy {w['old-heavy']:.1%}  new-heavy {w['new-heavy']:.1%}  blended {blended:.2%}  orders {blended*sessions:,.0f}")
    assert round(blended, 4) == 0.042
    assert round(blended * sessions) == 42_000
print("orders before:", 0.05 * sessions)
assert 0.05 * sessions == 50_000
# supply side: listings +25% -> avg listings per query result slot competing; sellers' orders per listing
orders_before, orders_after = 50_000, 42_000
listings_before, listings_after = 100_000, 125_000
opl_b, opl_a = orders_before / listings_before, orders_after / listings_after
print("orders per listing before/after:", opl_b, round(opl_a, 3), " change:", round(opl_a / opl_b - 1, 3))
assert opl_b == 0.5 and round(opl_a, 3) == 0.336 and round(opl_a / opl_b - 1, 3) == -0.328
