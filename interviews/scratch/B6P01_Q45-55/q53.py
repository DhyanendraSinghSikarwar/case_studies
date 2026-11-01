# Q53: volume / price / mix split of a Rs 100 crore -> Rs 112 crore revenue change (illustrative numbers)
# units in lakh, price in Rs per unit, revenue crore = lakh units x Rs / 100
tiers = ["standard", "premium"]
u0 = {"standard": 75.0, "premium": 25.0}          # base units
p0 = {"standard": 80.0, "premium": 160.0}         # base price
R = lambda u, p: sum(u[t] * p[t] for t in tiers) / 100
V0 = sum(u0.values()); R0 = R(u0, p0)
assert V0 == 100.0 and R0 == 100.0

V1 = V0 * 1.06                                     # volume +6%
price_up = 1.02                                    # like-for-like price +2% in every tier
p1 = {t: p0[t] * price_up for t in tiers}
# choose the new premium share so that revenue is exactly 112 crore
s = (112 * 100 / V1) / p1["standard"] - 1          # avg price = p_std1 * (1 + s) since premium = 2x standard
u1 = {"standard": V1 * (1 - s), "premium": V1 * s}
R1 = R(u1, p1)
print(f"new units: standard {u1['standard']:.2f}, premium {u1['premium']:.2f} lakh; premium share {s:.1%} (was 25.0%); revenue {R1:.3f} crore")
assert abs(R1 - 112) < 1e-9 and abs(s - 0.2948) < 5e-4

# ORDER 1: volume (at base mix and base price) -> mix (at base prices) -> price (at new volume and mix)
vol1 = (V1 - V0) * R0 / V0
mix1 = R(u1, p0) - V1 * R0 / V0
price1 = R1 - R(u1, p0)
print(f"order 1 volume, mix, price: {vol1:.2f}  {mix1:.2f}  {price1:.2f}  total {vol1+mix1+price1:.2f}")
assert round(vol1, 2) == 6.00 and round(mix1, 2) == 3.80 and round(price1, 2) == 2.20
assert abs(vol1 + mix1 + price1 - 12) < 1e-9

# ORDER 2: price (at base volume and mix) -> volume (at new price) -> mix (the rest)
price2 = R(u0, p1) - R0
vol2 = (V1 - V0) * R(u0, p1) / V0
mix2 = (R1 - R0) - price2 - vol2
print(f"order 2 price, volume, mix: {price2:.2f}  {vol2:.2f}  {mix2:.2f}  total {price2+vol2+mix2:.2f}")
assert round(price2, 2) == 2.00 and round(vol2, 2) == 6.12 and round(mix2, 2) == 3.88

# the wording check: if "+2%" were the BLENDED average price, volume x price alone gives:
print("volume x blended price only:", round(100 * 1.06 * 1.02, 2), "crore (not 112)")
assert round(100 * 1.06 * 1.02, 2) == 108.12
print("realised average price change:", round((R1 / V1) / (R0 / V0) - 1, 4))
assert round((R1 / V1) / (R0 / V0) - 1, 4) == 0.0566
