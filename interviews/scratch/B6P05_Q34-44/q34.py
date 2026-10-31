import math
emails = 5_000_000
clicks_base, clicks_new = 0.020 * emails, 0.022 * emails
extra_clicks = clicks_new - clicks_base
click_value = extra_clicks * 3.00
unsub_extra = (0.0012 - 0.0010) * emails
unsub_cost = unsub_extra * 12
cost = 15_000
net = click_value - cost - unsub_cost
print(f"extra clicks {extra_clicks:,.0f}; click margin {click_value:,.0f}")
print(f"extra unsubscribes {unsub_extra:,.0f}; future margin lost {unsub_cost:,.0f}")
print(f"net weekly value {net:,.0f}")
assert round(extra_clicks) == 10_000 and round(click_value) == 30_000
assert round(unsub_extra) == 1_000 and round(unsub_cost) == 12_000
assert round(net) == 3_000
assert abs(0.022 / 0.020 - 1 - 0.10) < 1e-9
be = (cost + unsub_cost) / extra_clicks
print(f"break-even margin per extra click {be:.2f}")
assert abs(be - 2.70) < 1e-9
for m in (3.00, 2.70, 2.00):
    print(f"  margin/click {m:.2f} -> net {extra_clicks*m - cost - unsub_cost:,.0f}")
# noise check, assuming (illustrative) 2.5M emails per arm
n = emails / 2
def z(p1, p2):
    p = (p1 + p2) / 2
    return (p2 - p1) / math.sqrt(2 * p * (1 - p) / n)
zc, zu = z(0.020, 0.022), z(0.0010, 0.0012)
print(f"z for clicks {zc:.1f}, z for unsubscribes {zu:.1f} (2.5M per arm, assumed)")
assert zc > 10 and zu > 5
# thin cushion: a 10% miss on the click value flips the sign
print(f"net if click value is 10% lower: {0.9*click_value - cost - unsub_cost:,.0f}")
assert abs(0.9 * click_value - cost - unsub_cost) < 1e-6
