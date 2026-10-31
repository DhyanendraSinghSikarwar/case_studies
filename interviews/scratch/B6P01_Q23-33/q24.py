# Q24 open rate 20% -> 45% from machine opens (illustrative numbers)
sends = 100_000
apple_share = 0.5                  # share of sends delivered to a client that pre-fetches the pixel
open_before = {"proxy": 0.20, "other": 0.20}
open_after = {"proxy": 0.70, "other": 0.20}   # proxy opens now include machine opens
click_rate_per_send = 0.02         # unchanged in both groups, both periods

def blended(d):
    return apple_share * d["proxy"] + (1 - apple_share) * d["other"]

ob, oa = blended(open_before), blended(open_after)
opens_b, opens_a = round(ob * sends), round(oa * sends)
ob, oa = round(ob, 4), round(oa, 4)
clicks = round(click_rate_per_send * sends)
ctor_b, ctor_a = clicks / opens_b, clicks / opens_a
print("open rate before/after:", ob, oa)
print("opens before/after:", opens_b, opens_a)
print("clicks (both periods):", clicks)
print("click-to-open before/after:", round(ctor_b, 3), round(ctor_a, 3))
print("open rate non-proxy only, before/after:", open_before["other"], open_after["other"])
assert round(ob, 2) == 0.20 and round(oa, 2) == 0.45
assert opens_b == 20000 and opens_a == 45000
assert clicks == 2000
assert round(ctor_b, 3) == 0.100 and round(ctor_a, 3) == 0.044
assert open_after["other"] == open_before["other"]
# proxy-adjusted metric: count opens only from non-proxy clients, or use clicks per delivered
print("clicks per delivered:", clicks / sends)
assert clicks / sends == 0.02
