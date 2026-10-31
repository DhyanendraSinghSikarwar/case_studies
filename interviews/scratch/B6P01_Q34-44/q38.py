# Q38 conversion 3.0% -> 3.6% with orders flat (illustrative numbers)
before = dict(sessions=1_000_000, bot_sessions=166_667, orders=30_000)
after_ = dict(sessions=1_000_000, bot_sessions=166_667, orders=30_000)   # same traffic; filter now removes bots

raw_before = before["orders"] / before["sessions"]
filtered_after = after_["orders"] / (after_["sessions"] - after_["bot_sessions"])
restated_before = before["orders"] / (before["sessions"] - before["bot_sessions"])
print(f"reported before (no filter): {raw_before:.2%}")
print(f"reported after  (filter on): {filtered_after:.2%}")
print(f"restated before (filter on): {restated_before:.2%}")
print(f"like-for-like change: {filtered_after - restated_before:+.3%} points; orders change: {after_['orders']-before['orders']:+d}")
assert round(raw_before, 4) == 0.03 and round(filtered_after, 4) == 0.036 and round(restated_before, 4) == 0.036
assert after_["orders"] == before["orders"]

# if the filter also removes some real humans (false positives that never buy), the restated lift is partly an artefact
# 10,000 humans wrongly removed, none of them buyers: denominator shrinks further with no extra orders
human = before["sessions"] - before["bot_sessions"]
fp = 10_000
with_fp = before["orders"] / (human - fp)
print(f"with 10,000 non-buying humans wrongly filtered: {with_fp:.3%} (versus {restated_before:.3%} without)")
assert with_fp > restated_before

# a more honest primary metric when denominators are fragile: orders per eligible user (or per 1,000 humans)
print("orders per 1,000 filtered sessions after:", round(after_['orders'] / (after_['sessions'] - after_['bot_sessions']) * 1000, 1))
# per-user view: distinct buyers / distinct logged-in visitors is less exposed to session-definition changes
